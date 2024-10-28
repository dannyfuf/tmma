from gis import Point

from tmma import Snap
from tmma.snapping.validate_snap import ValidateSnap

class SnapToRoad:
    def __init__(
        self,
        distance_index,
        road_graph,
        route,
        point,
        speed_tolerance
    ):
        self.distance_index = distance_index
        self.road_graph = road_graph
        self.route = route
        self.point = point
        self.speed_tolerance = speed_tolerance

    def run(self):
        possible_snap = self._get_possible_snap(self.point)

        # only true in first iteration
        if len(self.route) == 0:
            self._add_snap_to_route(possible_snap)
            return

        route = self._get_route(possible_snap)
        if len(route) == 0:
            print(f'skipping id: {possible_snap.point.id() - 1}')
            self.snap_in_current_iteration = False
            return

        last_snap = self._get_last_snap()
        self.snap_in_current_iteration = ValidateSnap(
            route=route,
            possible_snap=possible_snap,
            last_snap=last_snap,
            road_graph=self.road_graph,
            speed_tolerance=self.speed_tolerance
        ).run()
        if self.snap_in_current_iteration:
            self._add_snap_to_route(possible_snap)

    def _get_possible_snap(self, point: Point):
        closest_road = self.distance_index.get_closest_road(point)
        projected_point = closest_road.project(point)
        possible_snap = Snap(point, closest_road, projected_point)
        return possible_snap

    def _add_snap_to_route(self, possible_snap: Snap):
        self.route.append(possible_snap)

    def _get_route(self, possible_snap: Snap):
        last_snapped_road_id = self.route[-1].road.id()
        route = self.road_graph.compute_route(
            last_snapped_road_id,
            possible_snap.road.id()
        )
        return route

    def _get_last_snap(self):
        return self.route[-1]