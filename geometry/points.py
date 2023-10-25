from qgis.core import *

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

# ------------------------------------------------------------
#                         GETTERS
# ------------------------------------------------------------