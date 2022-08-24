import os
import sys
import argparse
import logging
import pandas as pd
import xarray as xr
import monetio as mio

from datetime import datetime
from melodies_monet.util import write_util


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

    dates_daily = pd.date_range(start=args.start, end=args.end, freq='d')
    logging.debug(dates_daily)
    datestrs_daily = [date.strftime('%Y%m%d') for date in dates_daily]
    logging.debug(datestrs_daily)


