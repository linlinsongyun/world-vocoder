import time
import sys
import os
import shutil

model_dir = sys.argv[1]
save_dir = sys.argv[2]
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

def mv_model(model_dir, save_dir):
    for fi in os.listdir(model_dir):
        if (fi.startswith('model-') & (len(fi)<32)):
            source_dir = os.path.join(model_dir, fi)
            if os.path.isfile(source_dir):
                tar_dir = os.path.join(save_dir, fi)
                shutil.move(source_dir, tar_dir)
                print('moved', fi)


def main():
    while(1):
        time.sleep(10)
        mv_model(model_dir, save_dir)
        print ("Current : %s" % time.ctime())        



if __name__ == '__main__':
    main()  


