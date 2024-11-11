from typing import List

from gis import Point, Layer, Line
from tmma import DistanceIndex, Snap
from tmma.road_graph.main import RoadGraph
from tmma.snapping.snap_to_road import SnapToRoad
from tmma.snapping.try_to_snap_with_neighbor_points import TryToSnapWithNeighborPoints
from tmma.snapping.get_points_without_snap import GetPointsWithoutSnap
from tmma.snapping.force_snap_for_remaining_points import ForceSnapForRemainingPoints
from tmma.snapping.get_result_roads import GetResultRoads
from tmma.snapping.build_snapped_roads_layer import BuildSnappedRoadsLayer
from tmma.snapping.build_snapped_points_layer import BuildSnappedPointsLayer

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
                self._current_point_idx = TryToSnapWithNeighborPoints(
                    self._distance_index,
                    self._road_graph,
                    self._route,
                    self._current_point_idx,
                    self._speed_tolerance,
                    6
                ).run()

            current_point = self._get_next_point()

        self._force_snap_to_remaining_points()

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
        return self._route[-1] if len(self._route) > 0 else None

    def _add_snap_to_route(self, possible_snap: Snap):
        self._route.append(possible_snap)

    def _force_snap_to_remaining_points(self):
        ForceSnapForRemainingPoints(
            self._distance_index,
            self._route,
            self._get_points_without_snap(),
            self._get_result_roads()
        ).run()

    def _get_points_without_snap(self):
        points_without_snap = GetPointsWithoutSnap(
            self._route,
            self._points
        ).run()
        return [point.id() for point in points_without_snap]

    def _get_result_roads(self):
        result_roads = GetResultRoads(self._route).run()
        return result_roads

    def build_snapped_roads_layer(self):
        return BuildSnappedRoadsLayer(
            self._route,
            self._road_layer
        ).run()

    def build_snapped_points_layer(self):
        return BuildSnappedPointsLayer(
            self._route,
            self._point_layer
        ).run()