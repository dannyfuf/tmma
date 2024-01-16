from qgis.core import *

from PyQt5.QtCore import QVariant

from geometry.layers import copy_feature

def create_line(
    object: QgsFeature
):
    return object.geometry()


def get_point_projection_on_line(
    point: QgsFeature,
    line: QgsFeature
):
    projected_point = line.geometry().closestSegmentWithContext(point.geometry().asPoint())[1]
    x, y = projected_point.x(), projected_point.y()
    new_point = copy_feature(point)
    new_point.setAttribute('X', x)
    new_point.setAttribute('Y', y)
    return new_point