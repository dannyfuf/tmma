from qgis.core import *

from geometry.lines import get_point_projection_on_line
from tmma.metrics import compute_speed_of_points

def check_snap(
    point_i: QgsFeature,
    point_j: QgsFeature,
    road_segment: QgsFeature,
    mean_speed: float,
    speed_tol: 1
)-> bool:
    feat_i_projection = get_point_projection_on_line(point_i, road_segment)
    feat_j_projection = get_point_projection_on_line(point_j, road_segment)

    points_projection_speed = compute_speed_of_points(
        feat_i_projection,
        feat_j_projection
    )
    return abs(mean_speed-points_projection_speed) < speed_tol
