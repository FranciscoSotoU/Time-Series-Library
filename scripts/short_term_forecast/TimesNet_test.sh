model_name=DLinear

python -u run.py \
  --exp_name DLinear_cafe_train_azucar_test\
  --virtual_present '2021-12-13' \
  --model_path Azucar_train_DLinear_PV:2021-12-13__DLinear_Sugar_500Exog.csv_sl52_ll26_pl52_0\
  --data_path Coffee_500Exog.csv \
  --task_name long_term_forecast \
  --is_training 0 \
  --model $model_name \
  --model_id coffee \
  --data custom \
  --root_path ./datasets/ \
  --features MS \
  --target value \
  --freq w \
  --seq_len 52 \
  --label_len 26 \
  --pred_len 52 \
  --seasonal_patterns None \
  --top_k 5 \
  --enc_in 501 \
  --dec_in 1 \
  --c_out 1 \
  --d_model 128 \
  --e_layers 3 \
  --d_layers 2 \
  --d_ff 64 \
  --factor 3 \
  --embed fixed \
  --num_workers 10 \
  --train_epochs 20 \
  --batch_size 128 \
  --patience 5 \
  --des 'Exp' \
  --lradj typeC \
  --pre_trained  \
  


