import os
import sys
melodies_dir = os.path.join(
    os.getenv('HOME'), 'EarthSystem', 'MELODIES-MONET')
monet_dir = os.path.join(
    os.getenv('HOME'), 'EarthSystem', 'monet')
monetio_dir = os.path.join(
    os.getenv('HOME'), 'EarthSystem', 'monetio')
sys.path.insert(0, melodies_dir)
sys.path.insert(0, monet_dir)
sys.path.insert(0, monetio_dir)
from melodies_monet import driver
import warnings
warnings.filterwarnings('ignore')

an = driver.analysis()
an.control = 'mm_musica.yaml'
an.read_control()
an.control_dict

an.open_models()
an.models

"""
an.open_obs()

an.pair_data()

for obs in an.obs:
    print(an.obs[obs])
    print(an.obs[obs].obj.info())
    print(an.obs[obs].obj.memory_usage())

an.plotting()
"""
