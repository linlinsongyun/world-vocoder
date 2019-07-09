import numpy as np
import sys
import os

ppgs_dir = sys.argv[1]
mel_dir = sys.argv[2]
save_dir = sys.argv[3]
dtype = sys.argv[4]

nor_lf0_dir = os.path.join(save_dir, 'nor-f0')

save_ppgs_path = os.path.join(save_dir,'comb_ppgs')
#female110
mean = 194.5283629854563
std = 42.612071139112906
if not os.path.exists(nor_lf0_dir):
    os.makedirs(nor_lf0_dir)
if not os.path.exists(save_ppgs_path):
    os.makedirs(save_ppgs_path)

def infer_modify_f0(a, mean, std):
    value = []
    for i in range(a.shape[0]):
        if a[i] > 0.0:
            value.append(a[i])
    value = np.array(value, np.float64)
    a_mean = np.mean(value)
    a_std = np.std(value)
    print("f0_mean,f0_std",a_mean, a_std)
    #mean, std = cal_mean_std(f0_dir)
    print('f0.type',a.dtype)
    for i in range(a.shape[0]):
        if a[i] > 0.0:
            a[i] = np.exp(((np.log(a[i]) - np.log(a_mean))*np.log(std) / np.log(a_std)) + np.log(mean))
            a[i] = a[i]*1.1
            a[i] = np.log10(a[i])
    return a
    def train_modify_f0(f0):
    for i in range(f0.shape[0]):
        if f0[i] > 0.0:
            f0[i] = np.log10(f0[i])
    return f0

#give f0_file and modify woth one f0
def modify_f0(f0_path, f0_name, dtype, save_dir):
    f0 = np.fromfile(f0_path, np.float64)
    if dtype == 'infer':
        nor_lf0 = infer_modify_f0(f0, mean, std)
    elif dtype == 'train':
        nor_lf0 = train_modify_f0(f0)
    print('save_dir',save_dir)

    nor_lf0_path = os.path.join(save_dir, 'nor-f0', f0_name)
    print('nor_lf0_path',nor_lf0_path)
    np.save(nor_lf0_path, nor_lf0)
    print("saved", nor_lf0_path)
    # save *.npy
    #give ppgs_file and modify with one ppgs
def concat_ppgs_lf0_vuv(ppgs_file, file_name, vuv_dir, nor_lf0_dir, save_dir):
    # eg.file_name='p227_001.npy'
    name = file_name.split('.npy')[0]
    vuv_name = os.path.join(vuv_dir,'%s_vuv.npy'%name)
    print('vuv_dir',vuv_dir)
    print('vuv_name',vuv_name)
    vuv = np.load(vuv_name)
    nor_lf0_name = os.path.join(nor_lf0_dir, '%s.npy'%name)
    nor_lf0 = np.load(nor_lf0_name)
    ppgs = np.load(ppgs_file)
    ppgs = ppgs[:,:176]
    if(nor_lf0.shape[0] > ppgs.shape[0]):
        a = nor_lf0.shape[0] - ppgs.shape[0]
        nor_lf0 = nor_lf0[:-a]
        vuv = vuv[:-a]

    if(nor_lf0.shape[0]==ppgs.shape[0]):
        nor_lf0 = nor_lf0.reshape(nor_lf0.shape[0],1)
        vuv = vuv.reshape(vuv.shape[0],1)
        combin = np.hstack((ppgs, nor_lf0))
        combin = np.hstack((combin,vuv))
        print("combin",combin.shape)
        combin_path = os.path.join(save_dir,'comb_ppgs', file_name)
        np.save(combin_path, combin)
    else: print("%s lf0 dim not the same" % nor_lf0_path)
    #ppgs in one file
#f0 in different folders
#e.g. python comb_1_file.py ppgs_dir
def main():
    for fi in os.listdir(ppgs_dir):
        ppgs_file = os.path.join(ppgs_dir, fi)
        #f0 in */p227/f0/p227_001.f0
        folder_name =  fi.split('_',1)[0]
        file_name =  fi.split('.npy')[0]
        f0_file = os.path.join(mel_dir, '%s_16k'%folder_name,'f0', '%s.f0'%file_name)
        print('f0-file', f0_file)
        modify_f0(f0_file, fi, dtype, save_dir)
        vuv_dir =os.path.join(mel_dir, '%s_16k'%folder_name, 'cmpsub/vuv')
        concat_ppgs_lf0_vuv(ppgs_file, fi, vuv_dir, nor_lf0_dir, save_dir)

    print('end')
if __name__ == '__main__':
    main()
