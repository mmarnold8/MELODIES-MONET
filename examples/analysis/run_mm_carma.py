import os
import sys
import yaml

from glob import glob

monet_dir = os.path.join(
    os.getenv('HOME'), 'EarthSystem', 'monet')
monetio_dir = os.path.join(
    os.getenv('HOME'), 'EarthSystem', 'monetio')
sys.path.insert(0, monet_dir)
sys.path.insert(0, monetio_dir)

import monetio
from monetio.sat.hdfio import hdf_open, hdf_list, hdf_read

import warnings
warnings.filterwarnings('ignore')


def read_obs(config):

    for obs in config['obs']:
  
        files = sorted(
            glob(os.path.expandvars(config['obs'][obs]['files'])))

        for filename in files:
            print(filename)


def read_model(config):

    for model in config['model']:

        files = sorted(
            glob(os.path.expandvars(config['model'][model]['files'])))

        for filename in files:
            print(filename)



if __name__ == '__main__':

    config_file = 'mm_carma.yaml'

    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)

    print(config)

    read_obs(config)
    read_model(config)


