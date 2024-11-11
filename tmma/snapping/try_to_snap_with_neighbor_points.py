from tmma import Snap
from .snap_to_road import SnapToRoad

class TryToSnapWithNeighborPoints:
    def __init__(
            self,
            distance_index,
            road_graph,
            route,
            candidate_point_idx,
            speed_tolerance,
            max_neighbour_distance
        ):
        self.distance_index = distance_index
        self.road_graph = road_graph
        self.route = route
        self.speed_tolerance = speed_tolerance
        self.max_neighbour_distance = max_neighbour_distance
        self.number_of_points = len(distance_index.points())
        self.cursor_direction = 'backward'
        self.candidate_point_idx = candidate_point_idx
        self.current_candidate_point_idx = candidate_point_idx
        self.current_previous_snap_idx = 0

    def run(self):
        while self._should_try_another_neighbour():
            point, last_snap = self._get_point_and_last_snap()
            snap = SnapToRoad(
                self.distance_index,
                self.road_graph,
                point,
                last_snap,
                self.speed_tolerance
            ).run()
            if snap:
                # there is an error here in how the snaps in the middle of current_candidate_point_idx
                # and current_previous_snap_idx are removed and the error is bc the time difference
                # in the validation is zero (this must be bc is comparing the same point two times).
                # So a zero division error is generated
                self._update_route()
                self._add_snap_to_route(snap)
                break

        return self.current_candidate_point_idx

    def _get_point_and_last_snap(self):
        if self.cursor_direction == 'backward':
            point = self._get_point_in_idx(self.current_candidate_point_idx)
            last_snap = self._get_previous_snap(self.current_previous_snap_idx)
            self.cursor_direction = 'forward'
            self.current_previous_snap_idx += 1
            return point, last_snap

        point = self._get_point_in_idx(self.current_candidate_point_idx)
        last_snap = self._get_previous_snap(self.current_previous_snap_idx)
        self.cursor_direction = 'backward'
        self.current_candidate_point_idx += 1
        return point, last_snap


    def _get_point_in_idx(self, idx):
        if idx < 0 or idx >= self.number_of_points:
            return None

        return self.distance_index.points()[idx]

    def _get_previous_snap(self, idx):
        base_offset = 2 # is needed to skip the snap in position -1 because it was evaluated in the main execution
        computed_idx = idx + base_offset
        return self.route[::-1][computed_idx] if len(self.route) > computed_idx else None

    def _should_try_another_neighbour(self):
        return self._neighbours_distance() < self.max_neighbour_distance

    def _neighbours_distance(self):
        return self._forward_idx_distance() + self._backward_idx_distance()

    def _forward_idx_distance(self):
        return self.current_candidate_point_idx - self.candidate_point_idx

    def _backward_idx_distance(self):
        return self.current_previous_snap_idx + 2

    def _add_snap_to_route(self, possible_snap: Snap):
        self.route.append(possible_snap)

    def _update_route(self):
        snaps_to_remove = self.current_previous_snap_idx + 1
        del self.route[-snaps_to_remove:]