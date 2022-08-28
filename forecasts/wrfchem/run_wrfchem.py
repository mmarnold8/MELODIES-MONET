import sys
sys.path.append('../..')

from datetime import datetime
from melodies_monet import driver

import warnings
warnings.filterwarnings('ignore')

an = driver.analysis()
an.control = 'wrfchem.yaml'
an.read_control()

today_str = datetime.now().strftime('%Y%m%d')
an.control_dict['analysis']['start_time'].replace('today', today_str)
an.control_dict['analysis']['end_time'].replace('today', today_str)

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
