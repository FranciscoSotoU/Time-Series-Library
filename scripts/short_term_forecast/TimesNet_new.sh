
model_name=TimesNet

python -u run.py \
  --task_name long_term_forecast \
  --is_training 1 \
  --model $model_name \
  --model_id coffee \
  --data custom \
  --root_path ./dataset/pr \
  --data_path outputog.csv \
  --features S \
  --target value \
  --freq w \
  --seq_len 24 \
  --label_len 12 \
  --pred_len 24 \
  --seasonal_patterns None \
  --top_k 5 \
  --enc_in 1 \
  --dec_in 1 \
  --c_out 1 \
  --d_model 32 \
  --e_layers 3 \
  --d_layers 2 \
  --d_ff 64 \
  --factor 3 \
  --embed fixed \
  --num_workers 10 \
  --train_epochs 20 \
  --batch_size 32 \
  --patience 20 \
  --des 'Exp' \