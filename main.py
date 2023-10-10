import os
from qgis.core import *

# custom modules
from functions.preprocesing import tune_buffer_radius
from functions.qgis_utils import add_file_layer, print_layers

def main():
    # open gpkg file with layers
    add_file_layer(f'{os.getenv("DATA_PATH")}/portageroads.gpkg', 'portageroads')
    add_file_layer(f'{os.getenv("DATA_PATH")}/data_1140268103_10sec_1.gpkg', 'data_1140268103_10sec_1')

    print_layers()

    radius = tune_buffer_radius(
        roads_layer_name='portageroads',
        gps_layer_name='data_1140268103_10sec_1',
        radius_range=[1, 2],
        radius_step=1
    )
    print('radius: ', radius)
