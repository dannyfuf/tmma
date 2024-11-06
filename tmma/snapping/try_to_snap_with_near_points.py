from .snap_to_road import SnapToRoad

class TryToSnapWithNeighbourPoints:
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
        self.candidate_point_idx = candidate_point_idx
        self.speed_tolerance = speed_tolerance
        self.max_neighbour_distance = max_neighbour_distance
        self.number_of_points = len(distance_index.points())
        self.next_point_direction = 'backward'
        self.next_point_idx_diff = 0
        self.next_point = self.distance_index.points()[self.candidate_point_idx]
        self.previous_snap_idx_diff = 1
        self.previous_snap = self.route[-1]

    def run(self):
        while self._should_try_another_neighbour():
            point, last_snap = self._get_point_and_last_snap()
            snap = SnapToRoad(
                self.distance_index,
                self.road_graph,
                point,
                last_snap,
                self.speed_tolerance
            )
            if snap:
                self._add_snap_to_route(snap)
                return

    def _get_point_and_last_snap(self):
        if self.next_point_direction == 'backward':
            point = self.next_point
            last_snap = self._get_previous_snap()
            self.next_point_direction = 'forward'
            return point, last_snap

        point = self._get_next_point()
        last_snap = self.previous_snap
        self.next_point_direction = 'backward'
        return point, last_snap


    def _get_next_point(self):
        next_idx = self._get_next_idx()

        if next_idx:
            return self._get_next_candidate_point(next_idx)

    def _get_next_candidate_point(self):
        next_idx = self.candidate_point_idx + self.next_point_idx_diff

        if next_idx < 0 or next_idx >= self.number_of_points:
            return None

        self.next_point_idx_diff += 1
        return self.distance_index.points()[next_idx]

    def _get_previous_snap(self):
        previous_idx = -(self.previous_snap_idx_diff + 1)
        if previous_idx > len(self.route):
            return None

        self.previous_snap_idx_diff += 1
        return self.route[previous_idx]

    def _should_try_another_neighbour(self):
        return self._neighbours_distance() < self.max_neighbour_distance

    def _neighbours_distance(self):
        return self.next_point_idx_diff + self.previous_snap_idx_diff

    def _add_snap_to_route(self, possible_snap: Snap):
        self._route.append(possible_snap)