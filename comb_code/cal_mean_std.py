import numpy as np
import os
import sys

#f0_dir = 'test_0405/yy7_vuv.f0'
#nor_f0 = 'test_0405/yy7_vuvnor.f0'
f0_dir = sys.argv[1]
#print(nor_f0)
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
print("mean", a_mean)
print("std",a_std)
