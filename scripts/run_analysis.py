import os
import sys
sys.path.insert(0, '../../monetio')
sys.path.insert(0, '../../monet')
import argparse
import logging
import yaml
import numpy as np
import pandas as pd
import xarray as xr
from glob import glob
from analysis_utils import fill_date_template
from analysis_readers import read_mod08_m3
import warnings
warnings.filterwarnings('ignore')


def get_obs_vars(config):

    obs_vars_subset = dict()

    for model_name in config['model']:

        mapping = config['model'][model_name]['mapping']

        for obs_name in mapping:
            obs_vars = config['obs'][obs_name]['variables']
            obs_vars_subset[obs_name] = dict()

            for model_varname in mapping[obs_name]:
                obs_varname = mapping[obs_name][model_varname]
                obs_vars_subset[obs_name][obs_varname] \
                    = obs_vars[obs_varname]

    return obs_vars_subset


def read_models(config, date_str):

    for model_name in config['model']:

        datadir = config['model'][model_name]['datadir']
        filestr = config['model'][model_name]['filestr']
        filestr = fill_date_template(
            config['model'][model_name]['filestr'], date_str)
        files = glob(
            os.path.join(os.path.expandvars(datadir), filestr))
        logging.info(files)

        filename = files[0]
        ds_model = xr.open_dataset(filename)


def read_obs(config, obs_vars_subset, date_str):

    for obs_name in obs_vars_subset:

        datadir = config['obs'][obs_name]['datadir']
        filestr = fill_date_template(
            config['obs'][obs_name]['filestr'], date_str)
        files = glob(
            os.path.join(os.path.expandvars(datadir), filestr))
        logging.info(files)

        filename = files[0]
        file_extension = os.path.splitext(filename)[1]

        if obs_name == 'MOD08_M3':
            if file_extension == '.hdf':
                ds_obs = read_mod08_m3(filename, obs_vars_subset[obs_name])
            else:
                ds_obs = xr.open_dataset(filename)


def process_date(config, date):

    logging.info(date)
    date_str = date.strftime('%Y-%m-%d-%j')

    obs_vars = get_obs_vars(config)
    logging.info(obs_vars)

    read_models(config, date_str)

    read_obs(config, obs_vars, date_str)


def process(config):

    start_time = config['analysis']['start_time']
    end_time = config['analysis']['end_time']
    freq = config['analysis']['freq']

    dates = pd.date_range(
        start=start_time, end=end_time, freq=freq)

    for date in dates:
        process_date(config, date)


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

