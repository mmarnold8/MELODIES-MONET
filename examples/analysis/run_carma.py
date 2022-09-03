import os
import sys
import yaml
import pandas as pd
import xarray as xr

from glob import glob

monet_dir = os.path.join(
    os.getenv('HOME'), 'EarthSystem', 'monet')
monetio_dir = os.path.join(
    os.getenv('HOME'), 'EarthSystem', 'monetio')
sys.path.insert(0, monet_dir)
sys.path.insert(0, monetio_dir)

import monetio
from monetio.sat.hdfio import hdf_open, hdf_close, hdf_list, hdf_read

import warnings
warnings.filterwarnings('ignore')


def process(config):

    start_time = config['analysis']['start_time']
    end_time = config['analysis']['end_time']
    freq = config['analysis']['freq']

    dates = pd.date_range(start=start_time, end=end_time, freq=freq)
    print(dates)

    for obs in config['obs']:

        files = sorted(
            glob(os.path.expandvars(config['obs'][obs]['files'])))

        for filename in files:
            print(filename)
            f = hdf_open(filename)
            datasets, indices = hdf_list(f)
            hdf_close(f)



if __name__ == '__main__':

    config_file = 'carma.yaml'

    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)

    process(config)


