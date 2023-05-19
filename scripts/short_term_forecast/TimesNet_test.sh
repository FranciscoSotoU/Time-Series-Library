model_name=DLinear

python -u run.py \
  --task_name long_term_forecast \
  --is_training 0 \
  --model $model_name \
  --model_id coffee \
  --data custom \
  --root_path ./datasets/ \
  --data_path sugar_test.csv \
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
  --model_path long_term_forecast_coffee_DLinear_custom_sugar_data.csv_bs128_lrtypeC_ftMS_sl52_ll26_pl52_dm128_nh8_el3_dl2_df64_fc3_ebfixed_dtTrue_Exp_0\


