from typing import List

from gis import Point, Layer, Line
from tmma import DistanceIndex, Snap
from tmma.road_graph.main import RoadGraph


class TMMA:
    _route: list[Snap]
    def __init__(self, distance_index: DistanceIndex, speed_tolerance: float = 1):
        self._distance_index = distance_index
        self._speed_tolerance = speed_tolerance
        self._road_layer = distance_index.road_layer()
        self._point_layer = distance_index.point_layer()
        self._road_graph = RoadGraph(self._road_layer)
        self._points = distance_index.points()
        self._current_point_idx = 0
        self._route = []

    def run(self):
        current_point = self._get_next_point()
        while current_point:
            self._snap_to_road(current_point)
            current_point = self._get_next_point()

    def _snap_to_road(self, point: Point):
        possible_snap = self._get_possible_snap(point)

        if len(self._route) == 0:
            self._add_snap_to_route(possible_snap)
            return

        route = self._get_route(possible_snap)
        print(f'route: {route}')

        if len(route) == 0:
            print(f'skipping id: {possible_snap.point.id() - 1}')
            return

        last_snap = self._get_last_snap()
        self._validate_snap(route, possible_snap, last_snap)

    def _validate_snap(self, route: List[Line], possible_snap: Snap, last_snap: Snap):
        computed_route_length = self._road_graph.compute_route_length(
            route,
            last_snap.projected_point,
            possible_snap.projected_point
        )

        time_difference = last_snap.point.time_to(possible_snap.point)
        computed_speed = self._compute_speed(computed_route_length, time_difference)
        mean_speed = self._compute_mean_speed(last_snap.point, possible_snap.point)

        if self._should_accept_snap(mean_speed, computed_speed):
            self._add_snap_to_route(possible_snap)
            print(f'route: {route} speed: {computed_speed} mean_speed: {mean_speed} -> accepted')
            return True

        print(f'route: {route} speed: {computed_speed} mean_speed: {mean_speed} -> rejected')
        return False

    def _get_possible_snap(self, point: Point):
        closest_road = self._distance_index.get_closest_road(point)
        projected_point = closest_road.project(point)
        possible_snap = Snap(point, closest_road, projected_point)
        return possible_snap

    def _add_snap_to_route(self, possible_snap: Snap):
        self._route.append(possible_snap)

    def _get_route(self, possible_snap: Snap):
        last_snapped_road_id = self._route[-1].road.id()
        route = self._road_graph.compute_route(
            last_snapped_road_id,
            possible_snap.road.id()
        )
        return route

    def _get_last_snap(self):
        return self._route[-1]

    def _should_accept_snap(self, mean_speed, computed_speed):
        speed_difference = abs(mean_speed - computed_speed)
        return speed_difference < self._speed_tolerance

    def _compute_speed(self, route_length, time_difference):
        return route_length / time_difference

    def _compute_mean_speed(self, start_point, end_point):
        return (start_point.speed() + end_point.speed()) / 2

    def _get_next_point(self):
        if self._current_point_idx < len(self._points):
            self._current_point_idx += 1
            return self._points[self._current_point_idx - 1]
        else:
            return None

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

