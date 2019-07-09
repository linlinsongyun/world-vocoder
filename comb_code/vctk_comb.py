import os
import sys
import  os.path
ppgs_dir = sys.argv[1]
mel_dir = sys.argv[2]
save_dir = sys.argv[3]

#p241
p241_mean = 116.3477758447432
p241_std = 14.010896276041622

list_dir = ['female111', 'female110', 'male107', 'male1085']

# infer with folders
'''
lenth = len(list_dir)
for i in range(lenth):
    nor_p = list_dir[i]
    mean = nor_p + '_mean'
    std = nor_p +'_std'
    #print('str mean, std', mean, std)
    mean = eval(mean)
    std = eval(std)
    #print('mean, std' ,mean, std)
    save_dir = os.path.join(save_dir, 'nor-%s'%nor_p)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    os.system('python comb_355_infer.py %s %s %s infer %.14f %.14f' %(ppgs_dir, mel_dir, save_dir, mean, std))
    print('saved', save_dir)

for f1 in os.listdir(mel_dir):
    mel_path = os.path.join(mel_dir, f1)
    if os.path.isdir(mel_path):
        name = f1[:4]
        ppgs_path = os.path.join(ppgs_dir, name)
        os.system('python comb_355_infer.py %s %s %s infer'%(ppgs_path, mel_path, save_dir))
        print('ppgs_path', ppgs_path)

print("end")
'''
#ppgs_dir is folders
for f1 in os.listdir(ppgs_dir):
    ppgs_path = os.path.join(ppgs_dir, f1)
    if os.path.isdir(ppgs_path):
        name = f1
        mel_path = os.path.join(mel_dir, name)
        os.system('python comb_355_infer.py %s %s %s train'%(ppgs_path, mel_path, save_dir))
        print('ppgs_path', ppgs_path)

print("done")
