class ValidateSnap:
    def __init__(
        self,
        road_graph,
        route,
        possible_snap,
        last_snap,
        speed_tolerance
    ):
        self.road_graph = road_graph
        self.route = route
        self.possible_snap = possible_snap
        self.last_snap = last_snap
        self.speed_tolerance = speed_tolerance


    def run(self):
        computed_route_length = self.road_graph.compute_route_length(
            self.route,
            self.last_snap.projected_point,
            self.possible_snap.projected_point
        )

        time_difference = self.last_snap.point.time_to(self.possible_snap.point)
        computed_speed = self._compute_speed(computed_route_length, time_difference)
        mean_speed = self._compute_mean_speed(self.last_snap.point, self.possible_snap.point)

        accept_snap = self._should_accept_snap(mean_speed, computed_speed, self.speed_tolerance)
        if accept_snap:
            print(f'route: {self.route} speed: {computed_speed} mean_speed: {mean_speed} -> accepted')
            return True

        print(f'route: {self.route} speed: {computed_speed} mean_speed: {mean_speed} -> rejected')
        return False

    def _should_accept_snap(self, mean_speed, computed_speed, speed_tolerance):
        speed_difference = abs(mean_speed - computed_speed)
        return speed_difference < speed_tolerance

    def _compute_speed(self, route_length, time_difference):
        return route_length / time_difference

    def _compute_mean_speed(self, start_point, end_point):
        return (start_point.speed() + end_point.speed()) / 2