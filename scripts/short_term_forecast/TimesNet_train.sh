model_name=TimesNet

python -u run.py \
  --exp_name S_Rolling_Azucar_train_TN\
  --virtual_present '2021-12-13' \
  --task_name long_term_forecast \
  --rolling 8\
  --integral 0\
  --is_training 1 \
  --model $model_name \
  --model_id coffee \
  --data custom \
  --root_path ./datasets/ \
  --data_path Coffee_500Exog.csv \
  --features S \
  --target value \
  --freq w \
  --seq_len 52 \
  --label_len 26 \
  --pred_len 52 \
  --seasonal_patterns None \
  --top_k 5 \
  --enc_in 1 \
  --dec_in 1 \
  --c_out 1 \
  --d_model 128 \
  --e_layers 3 \
  --d_layers 2 \
  --d_ff 64 \
  --factor 3 \
  --embed fixed \
  --num_workers 10 \
  --train_epochs 5 \
  --batch_size 128 \
  --patience 10 \
  --des 'Exp' \
  --lradj type1 \
  --no-pre_trained


