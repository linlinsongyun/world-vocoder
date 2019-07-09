#!/usr/bin/python
# -*- coding: <encoding name> -*-
import os
import glob
import numpy as np
import sys

####################################################################
#### save first 60-dim and 180-dim of the mgc features
# python others.py save_feat_60_180 (feat_root, save_root)
def f0_vuv(bin_name, save_name):
    if(bin_name.endswith('.f0')):
        a = open(bin_name)
        a = np.fromfile(a, np.float64)
        print(a.shape)
        np.savetxt(save_name,a)
    elif(bin_name.endswith('.mgc')):
        a = open(bin_name)
        a = np.fromfile(a, np.float32)
        print(a.shape)
        np.savetxt(save_name,a)
    elif(bin_name.endswith('.npy')):
        a = np.load(bin_name)
        np.savetxt(save_name, a)
        
if __name__ == "__main__":
    #import fire
    #fire.Fire()
    print("para list", str(sys.argv))
    f0_vuv(sys.argv[1], sys.argv[2])
