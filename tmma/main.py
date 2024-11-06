from typing import List

from gis import Point, Layer, Line
from tmma import DistanceIndex, Snap
from tmma.road_graph.main import RoadGraph
from tmma.snapping.snap_to_road import SnapToRoad
from tmma.snapping.try_to_snap_with_near_points import TryToSnapWithNeighbourPoints

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
        self.point_snapped = False

    def run(self):
        current_point = self._get_next_point()
        while current_point:
            self.snap_in_current_iteration = False
            self._snap_to_road(current_point)

            if not self.point_snapped:
                # based on the result of TryToSnapWithNeighbourPoints the next point could be
                # way ahead of the current point, so i need to consider this in the _get_next_point()
                # method. Maybe the command should return the id of the point snaped
                # FYI inside the TryToSnapWithNeighbourPoints the route is updated
                TryToSnapWithNeighbourPoints(
                    self._distance_index,
                    self.distance_index,
                    self._road_graph,
                    self._route,
                    self._current_point_idx,
                    self._speed_tolerance
                ).run()

            current_point = self._get_next_point()

    def _get_next_point(self):
        if self._current_point_idx < len(self._points):
            self._current_point_idx += 1
            return self._points[self._current_point_idx - 1]

    def _snap_to_road(self, point: Point):
        snap = SnapToRoad(
            self._distance_index,
            self._road_graph,
            point,
            self._get_last_snap(),
            self._speed_tolerance
        ).run()
        if snap:
            self._add_snap_to_route(snap)
            self.point_snapped = True
            return

        self.point_snapped = False
        return

    def _get_last_snap(self):
        return self._route[-1]

    def _add_snap_to_route(self, possible_snap: Snap):
        self._route.append(possible_snap)

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
