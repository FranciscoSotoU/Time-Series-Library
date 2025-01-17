import os
import numpy as np
import pandas as pd
import glob
import re
import torch
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import StandardScaler
from utils.timefeatures import time_features
from sktime.datasets import load_from_tsfile_to_dataframe
import warnings
from joblib import dump,load
warnings.filterwarnings('ignore')
from dateutil import relativedelta
from datetime import datetime




class Dataset_Custom(Dataset):
    def __init__(self, root_path, flag='train', size=None,
                 features='S', data_path='ETTh1.csv',
                 target='OT', scale=True, timeenc=0, freq='w',
                 seasonal_patterns=None,pre_trained=False,virtual_present = None,rolling=0,integral=False,rolling_times=0):
        # size [seq_len, label_len, pred_len]
        # info
        if size == None:
            self.seq_len = 24 * 4 * 4
            self.label_len = 24 * 4
            self.pred_len = 24 * 4
        else:
            self.seq_len = size[0]
            self.label_len = size[1]
            self.pred_len = size[2]
        # init
        assert flag in ['train', 'test', 'val']
        type_map = {'train': 0, 'val': 1, 'test': 2}
        self.set_type = type_map[flag]

        self.features = features
        self.target = target
        self.scale = scale
        self.timeenc = timeenc
        self.freq = freq
        
        self.evaluation = pre_trained
        self.root_path = root_path
        self.data_path = data_path
        self.virtual_present = datetime.strptime(virtual_present, "%Y-%m-%d")

        self.test_start = self.virtual_present 
        self.rolling = rolling
        self.rolling_times = rolling_times
        self.integral = integral
        self.__read_data__()

    def __read_data__(self):
        self.scaler = StandardScaler()
        df_raw = pd.read_csv(os.path.join(self.root_path,
                                          self.data_path))

        '''
        df_raw.columns: ['date', ...(other features), target feature]
        '''
        cols = list(df_raw.columns)
        cols.remove('date')
        if self.features == 'S' or self.features == 'MS':
            
            cols.remove(self.target)
        
            if 'id' in cols:
                cols.remove('id')

            df_raw = df_raw[['date'] + cols + [self.target]]
        else:

            df_raw = df_raw[['date'] + cols ]



        df_raw['date'] = pd.to_datetime(df_raw['date'])
        df_raw.set_index('date', drop=True)

        if self.rolling > 0:

            df_raw = df_raw.rolling(self.rolling,on='date',min_periods=1).sum()
   

        if self.integral>0:
            df_raw = df_raw.cumsum()
        

        if self.rolling_times>0:
            df_raw = self.create_rolling_dataset(df_raw)

        if self.evaluation:

            df_test = df_raw
            df_test = df_test[df_test['date'] >= self.test_start]
            num_train = 0
            num_test = int(len(df_test))

            num_vali = 0
            border1s = [0, num_train - self.seq_len, len(df_raw) - num_test - self.seq_len]
            border2s = [num_train, num_train + num_vali, len(df_raw)]

            border1 = len(df_raw) - num_test - self.seq_len
            border2 = len(df_raw)

            if self.features == 'M' or self.features == 'MS':
                cols_data = df_raw.columns[1:]
                df_data = df_raw[cols_data]
            elif self.features == 'S':
                df_data = df_raw[[self.target]]

            if self.scale:
                train_data = df_data
                self.scaler = load(self.data_path + '-scaler_train.joblib')
                
                data =self.scaler.transform(train_data)

            else:
                data = df_data.values

            df_stamp = df_raw[['date']][border1:border2]
            df_stamp['date'] = pd.to_datetime(df_stamp.date)
            if self.timeenc == 0:
                df_stamp['month'] = df_stamp.date.apply(lambda row: row.month, 1)
                df_stamp['day'] = df_stamp.date.apply(lambda row: row.day, 1)
                df_stamp['weekday'] = df_stamp.date.apply(lambda row: row.weekday(), 1)
                df_stamp['hour'] = df_stamp.date.apply(lambda row: row.hour, 1)
                data_stamp = df_stamp.drop(['date'], 1).values
            elif self.timeenc == 1:
                data_stamp = time_features(pd.to_datetime(df_stamp['date'].values), freq=self.freq)
                data_stamp = data_stamp.transpose(1, 0)

            self.data_x = data[border1:border2]
            
            self.data_y = data[border1:border2]
            
            self.data_stamp = data_stamp
            
            dates = pd.to_datetime(df_raw['date'])
            self.data_date = dates[border1:border2]
            



        else:
            df_train = df_raw
            df_train = df_train[df_train['date'] <= self.virtual_present]
            num_train = int(len(df_train))
            num_test = 0
            num_vali = 0#len(df_raw) - num_train - num_test
            border1s = [0, num_train - self.seq_len, len(df_raw) - num_test - self.seq_len]
            border2s = [num_train, num_train + num_vali, len(df_raw)]

            border1 = border1s[self.set_type]
            border2 = border2s[self.set_type]

            if self.features == 'M' or self.features == 'MS':
                cols_data = df_raw.columns[1:]
                df_data = df_raw[cols_data]
            elif self.features == 'S':
                df_data = df_raw[[self.target]]

            if self.scale:
                train_data = df_data[border1s[0]:border2s[0]]
                self.scaler.fit(train_data.values)
                data = self.scaler.transform(df_data.values)
                dump(self.scaler, self.data_path+'-scaler_train.joblib')

            else:
                data = df_data.values

            df_stamp = df_raw[['date']][border1:border2]
            df_stamp['date'] = pd.to_datetime(df_stamp.date)
            if self.timeenc == 0:
                df_stamp['month'] = df_stamp.date.apply(lambda row: row.month, 1)
                df_stamp['day'] = df_stamp.date.apply(lambda row: row.day, 1)
                df_stamp['weekday'] = df_stamp.date.apply(lambda row: row.weekday(), 1)
                df_stamp['hour'] = df_stamp.date.apply(lambda row: row.hour, 1)
                data_stamp = df_stamp.drop(['date'], 1).values
            elif self.timeenc == 1:
                data_stamp = time_features(pd.to_datetime(df_stamp['date'].values), freq=self.freq)
                data_stamp = data_stamp.transpose(1, 0)


            self.data_x = data[border1:border2]
            
            self.data_y = data[border1:border2]
            
            self.data_stamp = data_stamp
            
            dates = pd.to_datetime(df_raw['date'])
            self.data_date = dates[border1:border2]

        
    def __getitem__(self, index):

        s_begin = index
        s_end = s_begin + self.seq_len
        r_begin = s_end - self.label_len
        r_end = r_begin + self.label_len + self.pred_len

        seq_x = self.data_x[s_begin:s_end]
        seq_y = self.data_y[r_begin:r_end]
        seq_x_mark = self.data_stamp[s_begin:s_end]
        seq_y_mark = self.data_stamp[r_begin:r_end]

        seq_x_date = self.data_date[s_begin:s_end].dt.strftime("%Y%m%d").astype(int)
        seq_y_date = self.data_date[r_begin:r_end].dt.strftime("%Y%m%d").astype(int)

        return seq_x, seq_y, seq_x_mark, seq_y_mark, seq_x_date.values, seq_y_date.values

    def __len__(self):
        return len(self.data_x) - self.seq_len - self.pred_len + 1

    def inverse_transform(self, data):
        if self.features == 'MS':
            scaler2 = StandardScaler()
            scaler2.scale_ = np.array(self.scaler.scale_[500])
            scaler2.mean_ = np.array(self.scaler.mean_[500])
            scaler2.var_ = np.array(self.scaler.var_[500])
            return scaler2.inverse_transform(data)
        if self.features == 'M':
            return self.scaler.inverse_transform(data)
    def create_rolling_dataset(self,dataset):
        df = dataset.copy()
        df = df[self.target]
        for i in range(1,self.rolling_times):
            df_roll_k = df.rolling(2**i).sum()
            df.join(df_roll_k,on='date')
        return df

