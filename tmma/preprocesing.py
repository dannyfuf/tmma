# from typing import Callable
# from qgis.core import *
# from math import inf

# # custom modules
# from geometries.layers import get_layer_by_name, get_object_count_in_layer, get_layer_features
# from geometries.points import create_point, create_buffer
# from geometries.lines import create_line
# from geometries.metrics import get_point_line_distance

# def tune_buffer_radius(
#     roads_layer_name: str,
#     gps_layer_name: str,
#     radius_range=[1, 10],
#     radius_step: Callable[[int], int]=lambda x: 2*x
# ):
#     print('-----------------------------------------')
#     print('        starting tuning buffer')
#     print('-----------------------------------------')
#     print('roads_layer_name: ', roads_layer_name)
#     print('gps_layer_name: ', gps_layer_name)
#     print('radius_range: ', radius_range)
#     print('radius_step: ', radius_step)
#     print('-----------------------------------------')

#     points_layer = get_layer_by_name(gps_layer_name)
#     len_points_layer = get_object_count_in_layer(points_layer)
#     if len_points_layer == 0:
#         print('no points in layer')
#         return

#     radius_range = map(radius_step, range(radius_range[0], radius_range[1]+1))
#     for radius in radius_range:
#         print('testing radius: ', radius)
#         points_within_road = 0

#         for point in get_layer_features(points_layer):
#             point = create_point(point)
#             buffer = create_buffer(point, radius)
#             roads_layer = get_layer_by_name(roads_layer_name)

#             for feature in get_layer_features(roads_layer):
#                 road = feature.geometry()
#                 if road.intersects(buffer):
#                     points_within_road += 1
#                     break

#             coverage = points_within_road / len_points_layer
#             if coverage >= 0.99:
#                 print(f'radius found: {radius} with coverage: {coverage}')
#                 return radius

#     coverage = points_within_road / len_points_layer
#     print(f'radius found: {radius} with coverage: {coverage}')
#     return radius

# def filter_roads_in_radius(
#     roads_layer_name,
#     gps_layer_name,
#     radius
# ):
#     print('-----------------------------------------')
#     print('starting filtering roads in radius')
#     print('roads_layer_name: ', roads_layer_name)
#     print('gps_layer_name: ', gps_layer_name)
#     print('radius: ', radius)
#     print('-----------------------------------------')
#     points_layer = get_layer_by_name(gps_layer_name)
#     roads_layer = get_layer_by_name(roads_layer_name)

#     filtered_roads = []
#     for feature in roads_layer.getFeatures():
#         road = feature.geometry()
#         for point in points_layer.getFeatures():
#             point = create_point(point)
#             buffer = create_buffer(point, radius)
#             if road.intersects(buffer):
#                 filtered_roads.append(road)
#                 break
#     return filtered_roads

# def create_distance_index(
#     roads_layer_name,
#     gps_layer_name,
# ):
#     print('-----------------------------------------')
#     print('    starting creating distance index')
#     print('-----------------------------------------')
#     print('roads_layer_name: ', roads_layer_name)
#     print('gps_layer_name: ', gps_layer_name)
#     print('-----------------------------------------')
#     points_layer = get_layer_by_name(gps_layer_name)
#     roads_layer = get_layer_by_name(roads_layer_name)

#     distance_index = {}
#     for point in get_layer_features(points_layer):
#         road_distances = []
#         point_geometry = create_point(point)
#         for road in get_layer_features(roads_layer):
#             road_geometry = create_line(road)
#             distance = get_point_line_distance(point_geometry, road_geometry)
#             road_distances.append((road['fid'], distance))
#         road_distances.sort(key=lambda x: x[1])
#         distance_index[point['fid']] = road_distances
#     return distance_index

# def tune_buffer_radius_indexed(distance_index):
#     print('-----------------------------------------')
#     print('starting tuning buffer radius indexed')
#     print('-----------------------------------------')

#     min_distances = [distance_index[point_id][0][1] for point_id in distance_index]
#     min_distances.sort(reverse=True)
#     return min_distances[0]