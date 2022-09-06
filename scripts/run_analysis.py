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


def read_mod08_m3(filename, var_dict):

    ds_dict = dict()

    logging.info('read_mod08_m3:' + filename)
    f = hdf_open(filename)
    datasets, indices = hdf_list(f)

    lon = hdf_read(f, 'XDim')
    lat = hdf_read(f, 'YDim')
    lon_da = xr.DataArray(lon,
        attrs={'longname': 'longitude', 'units': 'deg East'})
    lat_da = xr.DataArray(lat,
        attrs={'longname': 'latitude', 'units': 'deg North'})

    for var in var_dict:
        logging.info('read_mod08_m3:' + var)
        data = np.array(hdf_read(f, var), dtype=float)
        data[data==var_dict[var]['fillvalue']] = np.nan
        var_da = xr.DataArray(
            data, coords=[lat_da, lon_da],
            dims=['lat', 'lon'])
        ds_dict[var] = var_da

    hdf_close(f)

    ds = xr.Dataset(ds_dict)
    ds.to_netcdf(filename.replace('.hdf', '.nc'))


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
                obs_vars = config['obs'][obs]['variables']

                obs_vars_subset = dict()
                for model_var in mapping[obs]:
                    obs_var = mapping[obs][model_var]
                    obs_vars_subset[obs_var] = obs_vars[obs_var]
                for filename in files:
                    if obs == 'MOD08_M3':
                        read_mod08_m3(filename, obs_vars_subset)


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

