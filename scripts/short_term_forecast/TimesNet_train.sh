model_name=TimesNet

python -u run.py \
  --task_name long_term_forecast \
  --is_training 1 \
  --model $model_name \
  --model_id coffee \
  --data custom \
  --root_path ./datasets/ \
  --data_path train_data.csv \
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
  --d_model 64 \
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
  --lradj type1 \
 


