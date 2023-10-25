from qgis.core import *

def get_point_line_distance(
    point: QgsGeometry,
    line: QgsGeometry
):
    return point.distance(line)