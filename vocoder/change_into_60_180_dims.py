import os=
import glob
import numpy as np

####################################################################
#### save first 60-dim and 180-dim of the mgc features
# python others.py save_feat_60_180 (feat_root, save_root)
def save_feat_60_180(feat_root, save_root):
    if not os.path.exists(save_root): os.makedirs(save_root)
    for feat_path in glob.glob(feat_root+'/*.cmp.npy'):
        feat = np.load(feat_path)
        feat_60 = feat[:, :60]
        feat_180 = feat[:, :180]
        feat_name = os.path.basename(feat_path)
        save_path_60 = os.path.join(save_root, feat_name+'.60.npy')
        save_path_180 = os.path.join(save_root, feat_name+'.180.npy')
        np.save(save_path_60, feat_60)
        np.save(save_path_180, feat_180)


if __name__ == "__main__":
    import fire
    fire.Fire()
