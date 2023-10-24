from typing import Callable
from qgis.core import *

# custom modules
from functions.layers import get_layer_by_name, get_object_count_in_layer, get_layer_features
from functions.points import create_point, create_buffer

def tune_buffer_radius(
    roads_layer_name: str,
    gps_layer_name: str,
    radius_range=[1, 10],
    radius_step: Callable[[int], int]=lambda x: 2*x
):
    print('-----------------------------------------')
    print('        starting tuning buffer')
    print('-----------------------------------------')
    print('roads_layer_name: ', roads_layer_name)
    print('gps_layer_name: ', gps_layer_name)
    print('radius_range: ', radius_range)
    print('radius_step: ', radius_step)
    print('-----------------------------------------')

    points_layer = get_layer_by_name(gps_layer_name)
    len_points_layer = get_object_count_in_layer(points_layer)
    if len_points_layer == 0:
        print('no points in layer')
        return

    radius_range = map(radius_step, range(radius_range[0], radius_range[1]+1))
    for radius in radius_range:
        print('testing radius: ', radius)
        points_within_road = 0

        for point in get_layer_features(points_layer):
            point = create_point(point)
            buffer = create_buffer(point, radius)
            roads_layer = get_layer_by_name(roads_layer_name)

            for feature in get_layer_features(roads_layer):
                road = feature.geometry()
                if road.intersects(buffer):
                    points_within_road += 1
                    break

            coverage = points_within_road / len_points_layer
            if coverage >= 0.99:
                print(f'radius found: {radius} with coverage: {coverage}')
                return radius
    
    coverage = points_within_road / len_points_layer
    print(f'radius found: {radius} with coverage: {coverage}')
    return radius

def filter_roads_in_radius(
    roads_layer_name,
    gps_layer_name,
    radius
):
    print('-----------------------------------------')
    print('starting filtering roads in radius')
    print('roads_layer_name: ', roads_layer_name)
    print('gps_layer_name: ', gps_layer_name)
    print('radius: ', radius)
    print('-----------------------------------------')
    points_layer = get_layer_by_name(gps_layer_name)
    roads_layer = get_layer_by_name(roads_layer_name)

    filtered_roads = []
    for feature in roads_layer.getFeatures():
        road = feature.geometry()
        for point in points_layer.getFeatures():
            point = create_point(point)
            buffer = create_buffer(point, radius)
            if road.intersects(buffer):
                filtered_roads.append(road)
                break
    return filtered_roads