import os
import sys
import argparse
import logging
import pandas as pd
import xarray as xr
import monetio as mio

from datetime import datetime, timedelta

from melodies_monet.util import write_util

def make_datetime_list(datestr_start, datestr_end, jday=False):
    """
    Generate a contiguous list of date strings.
    Params:
        datestr_start (str, yyyymmdd): start date
        datestr_end (str, yyyymmdd): end date
        jday (bool) : return yyyyddd (day of year) format
    Returns:
        list of datetime strings (str, yyyymmdd or yyyyddd)
    """
    datetime_start = datetime.strptime(datestr_start, '%Y%m%d')
    datetime_end = datetime.strptime(datestr_end, '%Y%m%d')
    logging.debug(datetime_start)
    logging.debug(datetime_end)
    ndays = (datetime_end - datetime_start).days + 1
    logging.debug(ndays)
    datetimes = [datetime_start + timedelta(days=i) for i in range(ndays)]
    if jday:
        datelist = [date.strftime('%Y%j') for date in datetimes]
    else:
        datelist = [date.strftime('%Y%m%d') for date in datetimes]
    return datelist


if __name__ == '__main__':

    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--datadir', type=str,
        default=os.path.join(os.getenv('HOME'), 'Data'),
        help='top-level data directory (default $HOME/Data)')
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

    datetime_list = make_datetime_list(args.start, args.end)
    logging.debug(datetime_list)


