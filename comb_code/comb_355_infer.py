import numpy as np
import os
import sys


ppgs_dir = sys.argv[1]
mel_dir = sys.argv[2]
save_dir = sys.argv[3]
stype = sys.argv[4]
#mean = sys.argv[5]
#std = sys.argv[6]
#already exists
f0_dir = os.path.join(mel_dir, 'f0')
vuv_dir = os.path.join(mel_dir, 'cmpsub/vuv')

# generate
nor_lf0_dir = os.path.join(mel_dir, 'f0')
male1085_mean = 108.83760335473913
male1085_std = 22.68180430188078
#list_dir = ['p241','p245', 'p246','p251','p255','p276', 'p277','p280','p282','p283']
#list_dir = ['p241','p245', 'p246','p251','p255']

list_dir = ['female111', 'female110', 'male107', 'male1085']
#list_dir = ['p241','p245', 'p246','p248','p249','p251','p253','p255']
#list_dir = ['p241','p245', 'p246','p251','p255']
#list_dir = ['p306', 'p283','p300','p310','p312']
#list_dir = ['p226','p252','p266','p303']
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
if not os.path.exists(nor_lf0_dir):
    os.makedirs(nor_lf0_dir)

def cal_mean_std(f0_dir):
    value = []
    for fi in os.listdir(f0_dir):
        if fi.endswith('.f0'):
            fi_name = os.path.join(f0_dir, fi)
            a = open(fi_name)
            a = np.fromfile(a, np.float64)
            for i in range(a.shape[0]):
                if a[i] > 0.0:
                    value.append(a[i])
    value = np.array(value, np.float64)
    a_mean = np.mean(value)
    a_std = np.std(value)
    return a_mean, a_std

# 1 nor with mean std
# 2 do with log
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
    def modify_f0(f0_dir, nor_lf0_dir, mean, std, stype):
    for fi in os.listdir(f0_dir):
        if fi.endswith('.f0'):
            name = fi.split('.f0')[0]
            f0_path = os.path.join(f0_dir, fi)
            nor_lf0_path = os.path.join(nor_lf0_dir, '%s_nor.lf0'%name)
            f0 = open(f0_path)
            f0 = np.fromfile(f0, np.float64)
            # do with mean and std
            if stype == 'infer':
                nor_lf0 = infer_modify_f0(f0, mean, std)
            elif stype == 'train':
                nor_lf0 = train_modify_f0(f0)
            np.array(nor_lf0, np.float64).tofile(nor_lf0_path)
            print("saved", nor_lf0_path)
            
  def concat_ppgs_lf0_vuv(vuv_dir, nor_lf0_dir, ppgs_dir, mel_dir, save_dir):
    for fi in os.listdir(ppgs_dir):
        ppgs_path = os.path.join(ppgs_dir, fi)
        print("ppgs_path", ppgs_path)
        name = fi.split('.npy')[0]
        vuv_name = name + '_vuv.npy'
        nor_lf0_name = name + '_nor.lf0'
        vuv_path = os.path.join(vuv_dir, vuv_name)
        nor_lf0_path = os.path.join(nor_lf0_dir, nor_lf0_name)
        nor_lf0 = open(nor_lf0_path)
        print("nor_lf0",nor_lf0_path)
        nor_lf0 = np.fromfile(nor_lf0, np.float64)
        ppgs = np.load(ppgs_path)
        vuv = np.load(vuv_path)
        print("ppgs", ppgs.shape)
        print("nor_lf0", nor_lf0.shape)
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
            combin_path = os.path.join(save_dir, '%s.npy' % name)
            np.save(combin_path, combin)
        else: print("%s lf0 dim not the same" % nor_lf0_path)
       '''
# do infer
def main():
    lenth = len(list_dir)
    for i in range(lenth):
        nor_p = list_dir[i]
        mean = nor_p + '_mean'
        std = nor_p +'_std'
        #print('str mean, std', mean, std)
        mean = eval(mean)
        std = eval(std)
        print('mean, std' ,mean, std)
        save_path = os.path.join(save_dir, 'nor-%s'%nor_p)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        print('saved', save_dir)
        print("=========step 1 : nor and logf0===============")
        #modify_f0(f0_dir, nor_lf0_dir, mean, std, stype)
        #print("=========step 2: f02lf0 ===============")
        #f02lf0(sptk, mel_dir, nor_f0_dir, nor_lf0_dir)
        print("=========step 3: concat ppgs355===============")
        concat_ppgs_lf0_vuv(vuv_dir, nor_lf0_dir, ppgs_dir, mel_dir, save_path)
        print("all end")
'''
def main():
    print("=========step 1 : nor and logf0===============")
    modify_f0(f0_dir, nor_lf0_dir, mean, std, stype)
    print("=========step 3: concat ppgs355===============")
    concat_ppgs_lf0_vuv(vuv_dir, nor_lf0_dir, ppgs_dir, mel_dir, save_dir)
    print("all end")
    
if __name__ == '__main__':
    main()
              
                                             
