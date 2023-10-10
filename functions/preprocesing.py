from qgis.core import *
import qgis.utils

from qgis_utils import get_layer_by_name, get_object_count_in_layer, create_point, create_buffer#, create_layer_of_roads

def tune_buffer_radius(
    roads_layer_name,
    gps_layer_name,
    radius_range=[1, 10],
    radius_step=[2]
):
    print('-----------------------------------------')
    print('starting tuning buffer radius')
    print('roads_layer_name: ', roads_layer_name)
    print('gps_layer_name: ', gps_layer_name)
    print('radius_range: ', radius_range)
    print('radius_step: ', radius_step)
    print('-----------------------------------------')
    points_layer = get_layer_by_name(gps_layer_name)
    len_points_layer = get_object_count_in_layer(points_layer)

    for radius in range(radius_range[0], radius_range[1]+1, radius_step):
        print('testing radius: ', radius)
        points_within_road = 0

        for point in points_layer.getFeatures():
            point = create_point(point)
            buffer = create_buffer(point, radius)
            roads_layer = get_layer_by_name(roads_layer_name)

            for feature in roads_layer.getFeatures():
                road = feature.geometry()
                if road.intersects(buffer):
                    points_within_road += 1
                    break

            if points_within_road / len_points_layer >= 0.99:
                return radius
    return radius

# def filter_roads_in_buffer(
#     roads_layer_name,
#     gps_layer_name,
#     radius
# ):
#     point_layer = get_layer_by_name(gps_layer_name)
#     roads_layer = get_layer_by_name(roads_layer_name)
#     roads = []

#     for point in point_layer.getFeatures():
#         point = create_point(point)
#         buffer = create_buffer(point, radius)

#         for feature in roads_layer.getFeatures():
#             road = feature.geometry()
#             if road.intersects(buffer):
#                 roads.append(road)
#                 break
#     create_layer_of_roads(roads)
#     return roads

# def filter_roads_by_heading():
#     pass