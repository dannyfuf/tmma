from gis import Point

from tmma import Snap
from tmma.snapping.validate_snap import ValidateSnap

class SnapToRoad:
    def __init__(
        self,
        distance_index,
        road_graph,
        point,
        last_snap,
        speed_tolerance
    ):
        self.distance_index = distance_index
        self.road_graph = road_graph
        self.point = point
        self.last_snap = last_snap
        self.speed_tolerance = speed_tolerance

    def run(self):
        possible_snap = self._get_possible_snap(self.point)

        # only true in first iteration
        if self.last_snap is None:
            return possible_snap

        computed_route = self._get_route(possible_snap)
        if len(computed_route) == 0:
            print(f'skipping id: {possible_snap.point.id() - 1}')
            self.snap_in_current_iteration = False
            return

        last_snap = self.last_snap
        self.snap_in_current_iteration = ValidateSnap(
            route=computed_route,
            possible_snap=possible_snap,
            last_snap=last_snap,
            road_graph=self.road_graph,
            speed_tolerance=self.speed_tolerance
        ).run()

        if self.snap_in_current_iteration:
            return possible_snap

    def _get_possible_snap(self, point: Point):
        closest_road = self.distance_index.get_closest_road(point)
        projected_point = closest_road.project(point)
        possible_snap = Snap(point, closest_road, projected_point)
        return possible_snap

    def _get_route(self, possible_snap: Snap):
        last_snapped_road_id = self.last_snap.road.id()
        route = self.road_graph.compute_route(
            last_snapped_road_id,
            possible_snap.road.id()
        )
        return route