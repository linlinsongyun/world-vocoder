#### 准备数据
step1:自行提取ppgs，并且将ark转为每个wav单独保存的npy格式，命名为‘wav_name.npy'
step2:提取特征1
`python pre_fea_lpc.py wav_dir save_dir1`
在save_dir下生成mel_20、 out16 、 out32
step3:提取特征2 
`python step2-mgcExtraction.py --input=wav_dir --output=save_dir2`
`python change_into_60_180_dims.py save_feat_60_180 save_dir2/cmp save_dir2/cmpsub`
step4：准备特征3
`python cal_mean_std.py save_dir2/f0`得到mean/std
`python comb_355_infer.py ppgs_dir save_dir2 save_dir4 mean std`
#### infer
自行修改	`hparams/default.yaml`中的ppgs_path为save_dir4，mel_path为save_dir1/mel_20, save_path自定义
`python inference.py model_dir`
`python mel2wav.py save_path/gen new_save_dir`
