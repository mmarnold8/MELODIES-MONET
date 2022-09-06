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


def fill_date_template(template_str, datestr, datestr_jday):
    yyyy_str, mm_str, dd_str = tuple(datestr.split('-'))
    yyyy_str, ddd_str = tuple(datestr_jday.split('-'))

    if 'DDD' in template_str:
        return template_str.replace(
            'YYYY', yyyy_str).replace('DDD', ddd_str)
    else:
        return template_str.replace(
            'YYYY', yyyy_str).replace('MM', mm_str).replace('DD', dd_str)


def process(config):

    start_time = config['analysis']['start_time']
    end_time = config['analysis']['end_time']
    freq = config['analysis']['freq']

    dates = pd.date_range(
        start=start_time, end=end_time, freq=freq)
    datestrs = [date.strftime('%Y-%m-%d') for date in dates]
    datestrs_jday = [date.strftime('%Y-%j') for date in dates]

    for date, datestr, datestr_jday \
        in zip(dates, datestrs, datestrs_jday):

        for model in config['model']:
            datadir = config['model'][model]['datadir']
            filestr = config['model'][model]['filestr']
            filestr = fill_date_template(
                config['model'][model]['filestr'], datestr, datestr_jday)
            files = glob(
                os.path.join(os.path.expandvars(datadir), filestr))
            print(files)

            mapping = config['model'][model]['mapping']

            for obs in mapping:
                datadir = config['obs'][obs]['datadir']
                filestr = fill_date_template(
                    config['obs'][obs]['filestr'], datestr, datestr_jday)
                files = glob(
                    os.path.join(os.path.expandvars(datadir), filestr))
                print(files)

            """
            filename = ''
            print(filename)
            f = hdf_open(filename)
            datasets, indices = hdf_list(f)
            hdf_close(f)
            """


if __name__ == '__main__':

    config_file = '../examples/analysis/carma.yaml'

    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)

    process(config)


