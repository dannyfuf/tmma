from qgis.core import *
import qgis.utils

def get_layer_by_name(name):
    return QgsProject.instance().mapLayersByName(name)[0]

def get_object_count_in_layer(layer):
    return len(list(layer.getFeatures()))

def create_point(object, x_name='X', y_name='Y'):
    x, y = object[x_name], object[y_name]
    point_xy = QgsPointXY(x, y)
    return QgsGeometry.fromPointXY(point_xy)\

def create_buffer(point, radius, segments=5):
    return point.buffer(radius, segments)