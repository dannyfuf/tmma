import os
from qgis.core import *
from PyQt5.QtCore import QVariant

# custom modules
from geometry.project_control import add_file_layer, print_layers
from geometry.layers import get_layer_by_name, get_layer_features, get_layer_crs, save_layer_to_file, get_object_count_in_layer, search_feature_by, get_layer_fields
from geometry.layer_builder import LayerConfig, build_point_layer, build_line_layer, normalize_line_layer, normalize_point_layer
from geometry.points import get_time_between_points, get_distance_between_points, create_point
from geometry.lines import get_point_projection_on_line

from tmma.preprocesing import tune_buffer_radius, create_distance_index, tune_buffer_radius_indexed
from tmma.utils import get_path, load_distance_index
from tmma.metrics import compute_speed_mean, compute_speed_of_points
from tmma.snapping import snap

def main():
    # open gpkg file with layers
    add_file_layer(get_path('portageroads.gpkg'), 'portageroads')
    add_file_layer(get_path('data_1140268103_10sec_1.gpkg'), 'data_1140268103_10sec_1')

    print_layers()

    layer = get_layer_by_name('portageroads')
    converted_road_layer = normalize_line_layer(layer)
    save_layer_to_file(converted_road_layer, get_path('portageroads_normalized.gpkg'))

    layer = get_layer_by_name('data_1140268103_10sec_1')
    converted_points_layer = normalize_point_layer(layer)
    save_layer_to_file(converted_points_layer, get_path('data_1140268103_10sec_1_normalized.gpkg'))

    # add_file_layer(get_path('portageroads_normalized.gpkg'), 'portageroads_normalized')
    # add_file_layer(get_path('data_1140268103_10sec_1_normalized.gpkg'), 'data_1140268103_10sec_1_normalized')

    normalized_road_layer = get_layer_by_name('portageroads')
    normalized_points_layer = get_layer_by_name('data_1140268103_10sec_1')

    point1 = list(normalized_points_layer.getFeatures())[0]
    point2 = list(normalized_points_layer.getFeatures())[1]

    # create_distance_index('portageroads', 'data_1140268103_10sec_1')
    distance_index = load_distance_index()
    road_fid = distance_index[str(point1['fid'])][0][0]
    road_segment = search_feature_by(normalized_road_layer, f"fid = {road_fid}")[0]

    mean_speed = compute_speed_mean(normalized_points_layer)
    speed_threshold = 5
    snapped = snap(point1, point2, mean_speed, road_segment, speed_threshold)
    print(snapped)
