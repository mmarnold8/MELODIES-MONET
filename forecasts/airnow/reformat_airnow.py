import os
import sys
sys.path.append('../..')

import argparse
import logging
import pandas as pd
import xarray as xr
import monetio as mio

from datetime import datetime
from melodies_monet.util import write_util

import warnings
warnings.filterwarnings('ignore')


if __name__ == '__main__':

    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--datadir', type=str,
        default=os.path.join(os.getenv('HOME'), 'Data', 'AirNow'),
        help='top-level data directory (default $HOME/Data/AirNow)')
    parser.add_argument('--logfile', type=str,
        default=sys.stdout,
        help='log file (default stdout)')
    parser.add_argument('--debug', action='store_true',
        help='set logging level to debug')
    parser.add_argument('--start', type=str,
        default = datetime.now().strftime('%Y%m%d'),
        help='start date (yyyymmdd)')
    parser.add_argument('--end', type=str,
        default = datetime.now().strftime('%Y%m%d'),
        help='end date (yyyymmdd)')
    args = parser.parse_args()

    """
    Setup logging
    """
    logging_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(stream=args.logfile, level=logging_level)
    logging.info(args.datadir)

    dates_daily = pd.date_range(start=args.start, end=args.end, freq='d')
    dates_hourly = pd.date_range(start=args.start, end=args.end, freq='H')
    logging.debug(dates_daily)
    datestrs_daily = [date.strftime('%Y%m%d') for date in dates_daily]
    logging.debug(datestrs_daily)

    """
    Fetch AirNow data from AWS
    """
    df = mio.airnow.add_data(dates_daily, wide_fmt=False)
    logging.info(df.info())

    df = df.dropna(subset=['latitude', 'longitude']).rename(
        {'siteid': 'x'}, axis=1)
    logging.info(df.info())

    dfp = df.pivot_table(
        values='obs', index=['time', 'x'], columns=['variable'])
    logging.info(dfp.info())

    dfsite = df.drop(
        ['time', 'variable', 'obs'], axis=1).drop_duplicates(
         subset=['x']).set_index('x')
    logging.info(dfsite.info())

    """
    Create xarray Dataset
    """
    dfx = xr.merge([dfp.to_xarray(), dfsite.to_xarray()])
    logging.info(dfx)

    dfx['siteid'] = (('x'), dfx.x.values)
    dfx['x'] = range(len(dfx.x))
    dfx = dfx.expand_dims('y').set_coords(
        ['siteid', 'latitude', 'longitude']).transpose('time', 'y', 'x')
    logging.info(dfx)

    filename = os.path.join(args.datadir,
        'AirNow_' + args.start + '_' + args.end + '.nc')
    dfx.to_netcdf(filename)
    # write_util.write_ncf(dfx, filename)

