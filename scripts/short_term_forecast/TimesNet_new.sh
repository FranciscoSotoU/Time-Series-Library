export CUDA_VISIBLE_DEVICES=1

model_name=TimesNet

python -u run.py \
  --task_name short_term_forecast \
  --is_training 1 \
  --root_path ./dataset/pr \
  --data_path outputog.csv \
  --target value \
  --data coffe \
  --model_id coffee \
  --model $model_name \
  --features S \
  --e_layers 2 \
  --d_layers 1 \
  --factor 3 \
  --enc_in 1 \
  --dec_in 1 \
  --c_out 1 \
  --batch_size 16 \
  --d_model 32 \
  --d_ff 32 \
  --top_k 5 \
  --des 'Exp' \
  --itr 1 \
  --learning_rate 0.001 \
  --loss 'SMAPE' \
  --freq w \
  --train_epochs 1