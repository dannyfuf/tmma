from qgis.core import *

from geometry.lines import get_point_projection_on_line

from tmma.distance_index import DistanceIndex
from tmma.snapping import check_snap

class Snap:
    point_id: str
    road_id: str

    def __init__(self, point_id, road_id):
        self.point_id = point_id
        self.road_id = road_id

class Routing:
    distance_index: DistanceIndex
    mean_speed: float
    speed_tol: float
    last_snap: QgsFeature
    route: list[Snap]

    def __init__(self, distance_index, mean_speed, speed_tol):
        self.distance_index = distance_index
        self.mean_speed = mean_speed
        self.speed_tol = speed_tol
        self.last_snap = None
        self.route = []

    def add_snap(self, point_id, road_id):
        self.route.append(Snap(point_id, road_id))

    def snap_points(self, point_i, point_j):
        snapped = False
        while self.distance_index.set_next_candidate_road():
            road_candidate = self.distance_index.candidate_road()
            if check_snap(
                point_i,
                point_j,
                road_candidate,
                self.mean_speed,
                self.speed_tol
            ):
                self.add_snap(
                    point_j['fid'],
                    road_candidate['fid']
                )
                self.last_snap = get_point_projection_on_line(
                    point_j,
                    road_candidate
                )
                return True
        return 

    def compute_route(self):
        self.distance_index.set_next_point()
        projection_of_current_point = get_point_projection_on_line(
            self.distance_index.current_point(),
            self.distance_index.get_next_candidate_road()
        )
        self.last_snap = projection_of_current_point
        self.add_snap(
            self.distance_index.current_point_id(),
            self.distance_index.road_candidate_id()
        )

        while self.distance_index.set_next_point():
            point_i = self.last_snap
            point_j = self.distance_index.current_point()
            self.snap_points(point_i, point_j)

    def print_route(self):
        for snap in self.route:
            print(snap.point_id, snap.road_id)

