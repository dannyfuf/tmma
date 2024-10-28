from typing import List

from gis import Point, Layer, Line
from tmma import DistanceIndex, Snap
from tmma.road_graph.main import RoadGraph
from tmma.snapping.snap_to_road import SnapToRoad

class TMMA:
    _route: list[Snap]
    def __init__(
            self,
            distance_index: DistanceIndex,
            speed_tolerance: float = 1,
            point_position_distance: float = 5
        ):
        self._distance_index = distance_index
        self._speed_tolerance = speed_tolerance
        self._road_layer = distance_index.road_layer()
        self._point_layer = distance_index.point_layer()
        self._road_graph = RoadGraph(self._road_layer)
        self._points = distance_index.points()
        self._current_point_idx = 0
        self._route = []
        self.snap_in_current_iteration = False

    def run(self):
        current_point = self._get_next_point()
        while current_point:
            self.snap_in_current_iteration = False
            self._snap_to_road(current_point)
            current_point = self._get_next_point()

    def _get_next_point(self):
        if self._current_point_idx < len(self._points):
            self._current_point_idx += 1
            return self._points[self._current_point_idx - 1]
        else:
            return None

    def _snap_to_road(self, point: Point):
        SnapToRoad(
            self._distance_index,
            self._road_graph,
            self._route,
            point,
            self._speed_tolerance
        ).run()

    def build_snapped_roads_layer(self):
        roads = list(set([snap.road.feature() for snap in self._route]))
        return Layer().build(
            self._road_layer.type(),
            'snapped_roads',
            self._road_layer.crs_name(),
            self._road_layer.fields(),
            roads
        )

    def build_snapped_points_layer(self):
        snapped_points = [snap.projected_point.feature() for snap in self._route]

        return Layer().build(
            self._point_layer.type(),
            'snapped_points',
            self._point_layer.crs_name(),
            self._point_layer.fields(),
            snapped_points
        )

