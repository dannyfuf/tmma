from qgis.core import *

from geometry.lines import get_point_projection_on_line
from geometry.points import point_to_feature
from tmma.metrics import compute_speed_of_points

def snap(
    point_i: QgsFeature,
    point_j: QgsFeature,
    mean_speed: float,
    road_segment: QgsFeature,
    speed_tol: 1
)-> bool:
    feat_i_projection = get_point_projection_on_line(point_i, road_segment)
    feat_j_projection = get_point_projection_on_line(point_j, road_segment)

    points_projection_speed = compute_speed_of_points(
        feat_i_projection,
        feat_j_projection
    )

    print(abs(mean_speed-points_projection_speed))
    return abs(mean_speed-points_projection_speed) < speed_tol
