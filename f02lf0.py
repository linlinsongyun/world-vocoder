import os
import sys
import glob
import numpy as np
import argparse

mean = 244.4441646197036 
std = 66.65991277382562

def infer_modify_f0(a, mean, std):
    value = []
    uvu = np.zeros(a.shape[0])
    for i in range(a.shape[0]):
        if a[i] > 0.0:
            value.append(a[i])
    value = np.array(value, np.float64)
    a_mean = np.mean(value)
    a_std = np.std(value)
    for i in range(a.shape[0]):
        if a[i] > 0.0:
            uvu[i] = 1
            a[i] = np.exp(((np.log(a[i]) - np.log(a_mean))*np.log(std) / np.log(a_std)) + np.log(mean))
            a[i] = np.log10(a[i])
        else:
        	  uvu[i]=0  
    return a,uvu

def read_binfile(filename, dim=60, dtype=np.float64):
    fid = open(filename, 'rb')
    v_data = np.fromfile(fid, dtype=dtype)
    fid.close()
    if np.mod(v_data.size, dim) != 0:
        raise ValueError('Dimension provided not compatible with file size.')
    m_data = v_data.reshape((-1, dim)).astype('float64') 
    m_data = np.squeeze(m_data)
    return  m_data

def write_binfile(m_data, filename, dtype=np.float64):
    m_data = np.array(m_data, dtype)
    fid = open(filename, 'wb')
    m_data.tofile(fid)
    fid.close()
    return

def read_reaper_f0_file(est_file, skiprows=7):
    v_f0 = np.loadtxt(est_file, skiprows=skiprows, usecols=[2])
    v_f0[v_f0<0] = 0
    return v_f0

def reaper_f0_extract(in_wavfile, f0_file_ref, f0_file_out, frame_shift_ms=10.0):
    print("Running REAPER f0 extraction...")
    cmd = "%s -a -s -x 400 -m 70 -u %1.4f -e 0.01 -i %s -f %s" % ( 'bin/reaper', frame_shift_ms / 1000.0, in_wavfile, f0_file_out + "_reaper")
    os.system(cmd)
    v_f0_ref = read_binfile(f0_file_ref, dim=1)
    v_f0     = read_reaper_f0_file(f0_file_out + "_reaper")
    frm_diff = v_f0.size - v_f0_ref.size
    if frm_diff<0:
       v_f0 = np.r_[ v_f0, np.zeros(-frm_diff) + v_f0[-1]]
    if frm_diff>0:
        v_f0 = v_f0[:-frm_diff]
    write_binfile(v_f0, f0_file_out)
    return

if __name__ == '__main__':

  wav_file='1.wav'
  world_analysis_cmd = 'bin/analysis_10ms '+ wav_file + ' temp.f0_1 ' + ' temp.sp ' + ' temp.ap'
  os.system(world_analysis_cmd)
  reaper_f0_extract(wav_file, 'temp.f0_1', 'temp.f0')
  f0 = open('temp.f0')
  f0 = np.fromfile(f0, np.float64)
  nor_lf0, vuv = infer_modify_f0(f0, mean, std)
  ppgs = np.load('1.ppg.npy')
  np.array(vuv, np.float64)
  if(nor_lf0.shape[0] > ppgs.shape[0]):
    a = nor_lf0.shape[0] - ppgs.shape[0]
    nor_lf0 = nor_lf0[:-a]
    vuv = vuv[:-a]
  if(nor_lf0.shape[0]==ppgs.shape[0]):         
    nor_lf0 = nor_lf0.reshape(nor_lf0.shape[0],1)
    vuv = vuv.reshape(vuv.shape[0],1)
    combin = np.hstack((ppgs, nor_lf0))
    combin = np.hstack((combin,vuv))
    np.save('input.npy', combin)  
