from qgis.core import *

from geometry.points import get_point_speed, get_distance_between_points, get_time_between_points, create_point
from geometry.utils import feet_per_second_to_meters_per_second

def compute_speed_mean(layer: QgsVectorLayer):
    speed_sum = [get_point_speed(point) for point in layer.getFeatures()]
    feet_per_seconds = sum(speed_sum) / len(speed_sum)
    return feet_per_second_to_meters_per_second(feet_per_seconds)

def compute_speed_of_points(init: QgsFeature, end: QgsFeature):
    init_point = create_point(init)
    end_point = create_point(end)
    distance = get_distance_between_points(init_point, end_point)
    time = get_time_between_points(init, end)
    return distance / time
