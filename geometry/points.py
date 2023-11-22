from qgis.core import *
from datetime import datetime


from geometry.utils import feet_to_meters
# ------------------------------------------------------------
#                         BUILDERS
# ------------------------------------------------------------

def create_point(
    object: QgsFeature,
    x_name='X',
    y_name='Y'
):
    x, y = object[x_name], object[y_name]
    point_xy = QgsPointXY(x, y)
    return QgsGeometry.fromPointXY(point_xy)

def create_buffer(
    point: QgsGeometry,
    radius: float,
    segments=10
):
    return point.buffer(radius, segments)


def point_to_feature(
    point: QgsPointXY,
    fields: QgsFields
):
    feature = QgsFeature(fields)
    feature.setGeometry(point)
    return feature

# ------------------------------------------------------------
#                         GETTERS
# ------------------------------------------------------------

def get_distance_between_points(
    point_i: QgsGeometry,
    point_j: QgsGeometry
):
    return point_i.distance(point_j)

def get_time_between_points(
    point_i: QgsFeature,
    point_j: QgsFeature,
    field_name='Time'
):
    format = "%I:%M:%S %p"
    time_i = datetime.strptime(point_i[field_name], format)
    time_j = datetime.strptime(point_j[field_name], format)
    return (time_j - time_i).total_seconds()

def get_point_speed(point: QgsFeature, field_name='Speed'):
    return point[field_name]