from qgis.core import *

from geometry.utils import feet_to_meters

def get_point_line_distance(
    point: QgsGeometry,
    line: QgsGeometry
):
    distance_in_feet = point.distance(line)
    return feet_to_meters(distance_in_feet)