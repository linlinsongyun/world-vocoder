'''
Author: Lian Zheng
Target: Extract MGC features Using 16k sample audios
'''

import os
import sys
import glob
import argparse
from tools.acoustic_composition import AcousticComposition
from tools.extract_features import MGCParam

def generate_wavlist(wav_dir):
  wavlist = []
  for wavpath in glob.glob(wav_dir+'/*'):
    wavlist.append(wavpath)
  return wavlist


def world_feature_extraction(args):

  # read wav_list from wav_dir
  wav_list = generate_wavlist(args.input_dir)
  out_dir = args.output_dir

  ## extract (mgc,lf0,bap) features from wav_list 
  mgc = MGCParam()
  mgc.getMgc(wav_list, out_dir)
  
  print("get mgc done!!!")

  ## save all world features (only generate successfully)
  cmp_dir = os.path.join(out_dir, 'cmp')
  os.makedirs(cmp_dir, exist_ok=True)

  error_num = 0
  file_id_list = []
  mgc_list = []
  lf0_list = []
  bap_list = []
  world_cmp_list = []
  for line in wav_list:
      file_id = os.path.basename(line).split(".")[0]
      if not os.path.exists(os.path.join(out_dir, 'bap', file_id + '.bap')):
        error_num += 1
        continue
      file_id_list.append(file_id)
      mgc_list.append(os.path.join(out_dir, 'mgc', file_id + '.mgc'))
      lf0_list.append(os.path.join(out_dir, 'lf0', file_id + '.lf0'))
      bap_list.append(os.path.join(out_dir, 'bap', file_id + '.bap'))
      world_cmp_list.append(os.path.join(out_dir, 'cmp', file_id + '.cmp.npy'))

  print ('error samples: %d' %(error_num))

  ## convert world features into [187 dims] features
  acoustic_cmper = AcousticComposition()
  in_dimension_dict = { 'mgc' : 60, # 60
                        'bap' : 1, # 1
                        'lf0' : 1} # 1

  out_dimension_dict = { 'mgc' : 180, # 180
                         'vuv' : 1,     # 1
                         'bap' : 3, # 3
                         'lf0' : 3} # 3

  in_file_list_dict = {}
  in_file_list_dict['mgc'] = mgc_list
  in_file_list_dict['lf0'] = lf0_list
  in_file_list_dict['bap'] = bap_list
  acoustic_cmper.prepare_nn_data(in_file_list_dict, world_cmp_list, in_dimension_dict, out_dimension_dict)

  print('composition mgc vuv lf0 bap done!!!')
  print('all done!!!')



if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--input_dir', default='/home/lianzheng03/backup/baowei/wav-16000')
  parser.add_argument('--output_dir', default='baowei-Prepar16000')
  args = parser.parse_args()

  assert os.path.exists(args.input_dir)
  world_feature_extraction(args)