import os
from qgis.core import *
from PyQt5.QtCore import QVariant

# custom modules
from geometry.project_control import add_file_layer, print_layers
from geometry.layers import get_layer_by_name, get_layer_features, get_layer_crs, save_layer_to_file, get_object_count_in_layer
from geometry.layer_builder import LayerConfig, build_point_layer, build_line_layer

from tmma.preprocesing import tune_buffer_radius, create_distance_index, tune_buffer_radius_indexed
from tmma.utils import save_distance_index, load_distance_index

def main():
    # open gpkg file with layers
    add_file_layer(f'{os.getenv("DATA_PATH")}/portageroads.gpkg', 'portageroads')
    add_file_layer(f'{os.getenv("DATA_PATH")}/data_1140268103_10sec_1.gpkg', 'data_1140268103_10sec_1')

    print_layers()

    # radius = tune_buffer_radius(
    #     roads_layer_name='portageroads',
    #     gps_layer_name='data_1140268103_10sec_1',
    #     radius_range=[0, 1],
    #     radius_step=lambda x: 2**x
    # )
    # print(radius)


    # distance_index = create_distance_index(
    #     roads_layer_name='portageroads',
    #     gps_layer_name='data_1140268103_10sec_1',
    # )
    # save_distance_index(distance_index)

    distance_index = load_distance_index()
    min_dist = tune_buffer_radius_indexed(distance_index)
    print(min_dist)
