import os
import sys
sys.path.insert(0, '../../monetio')
sys.path.insert(0, '../../monet')
import argparse
import logging
import yaml
import pandas as pd
import xarray as xr
from glob import glob
import monetio
from monetio.sat.hdfio import hdf_open, hdf_close, hdf_list, hdf_read
import warnings
warnings.filterwarnings('ignore')


def fill_date_template(template_str, date_str):

    yyyy_str, mm_str, dd_str, ddd_str = tuple(date_str.split('-'))

    if 'DDD' in template_str:
        return template_str.replace(
            'YYYY', yyyy_str).replace('DDD', ddd_str)
    else:
        return template_str.replace(
            'YYYY', yyyy_str).replace('MM', mm_str).replace('DD', dd_str)


def read_mod08_m3(filename, var_list):

    logging.info('read_mod08_m3:' + filename)
    f = hdf_open(filename)
    datasets, indices = hdf_list(f)
    lon = hdf_read(f, 'XDim')
    lat = hdf_read(f, 'YDim')
    for var in var_list:
        logging.info('read_mod08_m3:' + var)
        data = hdf_read(f, var)
    hdf_close(f)


def process(config):

    start_time = config['analysis']['start_time']
    end_time = config['analysis']['end_time']
    freq = config['analysis']['freq']

    dates = pd.date_range(
        start=start_time, end=end_time, freq=freq)
    date_strs = [date.strftime('%Y-%m-%d-%j') for date in dates]

    for date, date_str in zip(dates, date_strs):

        logging.info(date)

        for model in config['model']:
            datadir = config['model'][model]['datadir']
            filestr = config['model'][model]['filestr']
            filestr = fill_date_template(
                config['model'][model]['filestr'], date_str)
            files = glob(
                os.path.join(os.path.expandvars(datadir), filestr))
            logging.info(files)

            mapping = config['model'][model]['mapping']

            for obs in mapping:
                datadir = config['obs'][obs]['datadir']
                filestr = fill_date_template(
                    config['obs'][obs]['filestr'], date_str)
                files = glob(
                    os.path.join(os.path.expandvars(datadir), filestr))
                logging.info(files)

                obs_list = list()
                for model_var in mapping[obs]:
                    obs_list.append(mapping[obs][model_var])
                for filename in files:
                    if obs == 'MOD08_M3':
                        read_mod08_m3(filename, obs_list)


if __name__ == '__main__':

    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--logfile', type=str,
        default=sys.stdout,
        help='log file (default stdout)')
    parser.add_argument('--debug', action='store_true',
        help='set logging level to debug')
    parser.add_argument('--config', type=str,
        default='../examples/analysis/carma.yaml')
    args = parser.parse_args()

    """
    Setup logging
    """
    logging_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(stream=args.logfile, level=logging_level)

    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)

    process(config)

