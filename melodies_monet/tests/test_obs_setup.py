import os
import sys
import argparse
import logging
import yaml

import math
import numpy as np
import scipy as sp
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('--control', type=str,
    default='control.yaml',
    help='yaml control file')
parser.add_argument('--logfile', type=str,
    default=sys.stdout,
    help='log file (default stdout)')
parser.add_argument('--debug', action='store_true',
    help='set logging level to debug')
args = parser.parse_args()

"""
Setup logging
"""
logging_level = logging.DEBUG if args.debug else logging.INFO
logging.basicConfig(stream=args.logfile, level=logging_level)

"""
Read YAML control
"""
with open(args.control, 'r') as f:
    control = yaml.safe_load(f)

start_time = pd.to_datetime(control['analysis']['start_time'])
end_time = pd.to_datetime(control['analysis']['end_time'])
datetime_indices = pd.date_range(start_time, end_time,
    freq=control['test_setup']['freq'])
print(datetime_indices)
ntime = len(datetime_indices)

"""
Generate random test observations
"""
np.random.seed(control['test_setup']['random_seed'])

var_names = control['obs']['test_obs']['variables'].keys()
df_dict = dict()
for var_name in var_names:
    df_dict[var_name] = np.random.rand(ntime)

df = pd.DataFrame(df_dict, index=datetime_indices)
print(df)
