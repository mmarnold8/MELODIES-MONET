import sys
sys.path.append('..')
from melodies_monet import driver
import warnings
warnings.filterwarnings('ignore')

an = driver.analysis()
an.control = 'wrfchem.yaml'
an.read_control()
an.control_dict

an.open_models()
an.models

an.open_obs()

an.pair_data()

for obs in an.obs:
    print(an.obs[obs])
    print(an.obs[obs].obj.info())
    print(an.obs[obs].obj.memory_usage())

# an.plotting()
