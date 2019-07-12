# Summary of MGC Feature Extraction

## Requirements

```sh
env: python3

pip install fire
pip install numpy
pip install multiprocessing
```



## Files List

 `bin/`:  execute tools

`tools/`: .py files for mgc extraction

`step2-mgcExtraction.py`: main file for feature extraction

`change_into_60_180_dims.py`: change 187-dim mgc into 60dim and 180dim

## Extract MGC features

- First, you need `python3`
- Then, step into `world_vocoder/ `folder


- Thrildly, `chmod -R 777 bin`


- Then, extract MGC Features

```sh
python step2-mgcExtraction.py --input=wav_root --output=save_root
# for example: python step2-mgcExtraction.py --input='ts2/wav-16000' --output='./ts2Results'
```

- Finally, you can get 
  - `save_root\bap\` 
  - `save_root\cmp\` : this is mgc features:    .npy files     feature_size: [frame_length, 187]
  - `save_root\f0\` 
  - `save_root\lf0\` 
  - `save_root\mgc\` 
  - `save_root\so\` 
- If you need 60 dim MGC or 180 dim MGC, you can run:

```sh
python change_into_60_180_dims.py save_feat_60_180 cmp_root save_root
# for example: python change_into_60_180_dims.py save_feat_60_180 ts2Results/cmp ts2Results/cmpsub
```

