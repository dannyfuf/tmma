from qgis.core import *

def create_line(
    object: QgsFeature
):
    return object.geometry()


def get_point_projection_on_line(
    point: QgsFeature,
    line: QgsFeature
):
    point = line.geometry().closestSegmentWithContext(point.geometry().asPoint())[1]
    return QgsGeometry.fromPointXY(point)