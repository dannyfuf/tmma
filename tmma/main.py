from gis import Point, Layer
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
        self._point_layer_mean_speed = self._distance_index.point_layer().get_mean_speed()
        self._current_point_idx = 0
        self._route = []
        print(f'mean speed: {self._point_layer_mean_speed}')

    #
    # runs the algorithm
    #
    def run(self):
        current_point = self._get_next_point()
        while current_point:
            self._snap_to_road(current_point)
            current_point = self._get_next_point()

    #
    # builds a layer with the snapped roads
    #
    def build_snapped_roads_layer(self):
        roads = list(set([snap.road.feature() for snap in self._route]))
        return Layer().build(
            self._road_layer.type(),
            'snapped_roads',
            self._road_layer.crs_name(),
            self._road_layer.fields(),
            roads
        )

    #
    # builds a layer with the snapped points projections
    #
    def build_snapped_points_layer(self):
        snapped_points = [snap.projected_point.feature() for snap in self._route]

        return Layer().build(
            self._point_layer.type(),
            'snapped_points',
            self._point_layer.crs_name(),
            self._point_layer.fields(),
            snapped_points
        )

    #
    # receives a point and computes the closest road to it
    # if is the first point of the route, then it accepts the snapping
    # otherwise it checks the criteria to accept the snapping
    #
    # first gets the last snapped point projection and the route it was snapped to
    # then computes a path that connects the road of the last snapped point
    # and the road of the current point
    # then computes the length of the route using the last snapped point projection
    # as the start point and the current point as the end point
    # then computes the speed of the route using the computed route length and
    # the time difference between the last snapped point and the current point
    # if the speed is lower than the tolerance, then it accepts the snapping
    #
    def _snap_to_road(self, point: Point):
        closest_road = self._distance_index.get_closest_road(point)
        projected_point = closest_road.project(point)

        if (len(self._route) == 0):
            self._route.append(Snap(point, closest_road, projected_point))
            return

        last_snapped_point_projection = self._route[-1].projected_point
        last_snapped_road_id = self._route[-1].road.id()
        route = self._road_graph.compute_route(last_snapped_road_id, closest_road.id())
        print(f'route: {route}')

        if route == []:
            print(f'skipping idx: {self._current_point_idx - 1}')
            return

        computed_route_length = self._road_graph.compute_route_length(
            route,
            last_snapped_point_projection,
            projected_point
        )

        last_snapped_point = self._route[-1].point
        time_difference = last_snapped_point.time_to(point)
        computed_speed = self._compute_speed(computed_route_length, time_difference)
        mean_speed = self._compute_mean_speed(last_snapped_point, point)
        if computed_speed < self._speed_tolerance:
            self._route.append(Snap(point, closest_road, projected_point))
            print(f'route: {route} speed: {computed_speed} mean_speed: {mean_speed} -> accepted')
            return

        print(f'route: {route} speed: {computed_speed} mean_speed: {mean_speed} -> rejected')

    #
    # checks if the snapping speed is lower than the tolerance
    # if it is returns true, otherwise returns false
    #
    def _should_accept_snap(self, mean_speed, computed_speed):
        speed_difference = abs(mean_speed - computed_speed)
        return speed_difference < self._speed_tolerance

    #
    # receives the route length and the time difference between the first point
    # and the last point and computes the speed of the route
    #
    def _compute_speed(self, route_length, time_difference):
        return route_length / time_difference


    def _compute_mean_speed(self, start_point, end_point):
        return (start_point.speed() + end_point.speed()) / 2
    # 
    # if there are any more points, then return the next point that is not in the route
    #
    def _get_next_point(self):
        if self._current_point_idx < len(self._points):
            self._current_point_idx += 1
            return self._points[self._current_point_idx - 1]
        else:
            return None

