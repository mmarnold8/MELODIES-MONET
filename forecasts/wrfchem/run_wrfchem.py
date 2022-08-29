import sys
sys.path.append('../..')

from datetime import datetime
from melodies_monet import driver

import warnings
warnings.filterwarnings('ignore')

an = driver.analysis()
an.control = 'wrfchem.yaml'
an.read_control()

date_str = datetime.now().strftime('%Y%m%d')
yyyy_str = date_str[0:4]
mm_str = date_str[4:6]
dd_str = date_str[6:8]

an.control_dict['analysis']['start_time'] \
    = an.control_dict['analysis']['start_time'].replace('today', date_str)
an.control_dict['analysis']['end_time'] \
    = an.control_dict['analysis']['end_time'].replace('today', date_str)

for model in an.control_dict['model']:
    an.control_dict['model'][model]['files'] \
        = an.control_dict['model'][model]['files'].replace(
            'YYYY', yyyy_str).replace('MM', mm_str).replace('DD', dd_str)

for obs in an.control_dict['obs']:
    an.control_dict['obs'][obs]['filename'] \
        = an.control_dict['obs'][obs]['filename'].replace(
            'YYYY', yyyy_str).replace('MM', mm_str).replace('DD', dd_str)

print(an.control_dict)

# an.open_models()
# an.models

# an.open_obs()

# an.pair_data()

# for obs in an.obs:
#     print(an.obs[obs])
#     print(an.obs[obs].obj.info())
#     print(an.obs[obs].obj.memory_usage())

# an.plotting()
