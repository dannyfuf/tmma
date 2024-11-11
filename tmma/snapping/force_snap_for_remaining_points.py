from gis import Layer, Point, Line

from tmma import Snap

class ForceSnapForRemainingPoints:
    def __init__(
        self,
        distance_index,
        route,
        remaining_points,
        roads_result,
    ):
        self.distance_index = distance_index
        self.route = route
        self.remaining_points = remaining_points
        self.roads_result = roads_result

    def run(self):
        for point in self.remaining_points:
            nearest_road = self._get_nearest_road_in_result(point)
            point = self._get_point(point)
            snap = self._snap_to_road(point, nearest_road)
            self.route.append(snap)

        self.route.sort(key=lambda x: x.point.id())


    def _get_nearest_road_in_result(self, point_id):
        point_distances = self.distance_index.get_distances_from_point(point_id)
        for distance in point_distances.frozen_distances:
            road_id = distance.road.id()
            if road_id in self.roads_result:
                return distance.road

    def _get_point(self, point_id):
        distances = self.distance_index.get_distances_from_point(point_id)
        return distances.point

    def _snap_to_road(self, point: Point, road: Line):
        projected_point = self._projected_point(point, road)
        snap = Snap(point, road, projected_point, None)
        return snap

    def _projected_point(self, point: Point, road: Line):
        projected_point = road.project(point)
        return projected_point