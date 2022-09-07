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
from analysis_utils import fill_date_template, find_file
from analysis_readers import read_gridded_eos
from analysis_plots import plot_lon_lat
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

    model_datasets = dict()

    for model_name in config['model']:

        datadir = config['model'][model_name]['datadir']
        filestr = config['model'][model_name]['filestr']
        filestr = fill_date_template(
            config['model'][model_name]['filestr'], date_str)
        filename = find_file(datadir, filestr)

        ds_model = xr.open_dataset(filename)

        model_datasets[model_name] = ds_model

    return model_datasets


def read_obs(config, obs_vars, date_str):

    obs_datasets = dict()

    for obs_name in obs_vars:

        data_format = config['obs'][obs_name]['data_format']
        datadir = config['obs'][obs_name]['datadir']
        filestr = fill_date_template(
            config['obs'][obs_name]['filestr'], date_str)
        filename = find_file(datadir, filestr)

        file_extension = os.path.splitext(filename)[1]

        if data_format == 'gridded_eos':
            if file_extension == '.hdf':
                ds_obs = read_gridded_eos(filename, obs_vars[obs_name])
            else:
                ds_obs = xr.open_dataset(filename)

        obs_datasets[obs_name] = ds_obs

    return obs_datasets


def plot_obs(config, date_str, obs_vars, obs_datasets):

    plotdir = os.path.expandvars(config['analysis']['output_dir'])

    for obs_name in obs_datasets:
        for obs_varname in obs_datasets[obs_name]:
            logging.info('plot_obs:%s,%s' % (obs_name, obs_varname))
            ds_obs = obs_datasets[obs_name][obs_varname]
            plot_params = obs_vars[obs_name][obs_varname]['plot_params']
            plot_params['outdir'] = plotdir
            plotname = fill_date_template(plot_params['name'], date_str)
            plotfile = obs_name + '_' + obs_varname + '_' + date_str

            plot_lon_lat(plotfile, plotname, plot_params, ds_obs)


def process_date(config, date):

    logging.info(date)
    date_str = date.strftime('%Y-%m-%d-%j')

    obs_vars = get_obs_vars(config)
    logging.info(obs_vars)

    # model_datasets = read_models(config, date_str)

    obs_datasets = read_obs(config, obs_vars, date_str)

    plot_obs(config, date_str, obs_vars, obs_datasets)


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

