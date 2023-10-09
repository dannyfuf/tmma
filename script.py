# qgis init
from qgis.core import *
import qgis.utils

# load custom modules
import os
import sys
modules_path = os.getcwd()
# check if platform is windows
if sys.platform == 'win32':
    modules_path = modules_path.replace('\\', '\\\\')

print('loading modules: ', modules_path)

# custom modules
from functions.preprocesing import tune_buffer_radius

radius = tune_buffer_radius(
    roads_layer_name='PortageRoads',
    gps_layer_name='data_1190268102_30sec_1',
    radius_range=[1, 2],
    radius_step=1
)
print('radius: ', radius)
