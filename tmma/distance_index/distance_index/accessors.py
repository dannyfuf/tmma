from typing import List

from gis import Point
from tmma.distance_index.distance_index_elements import IndexElement

class Accessors:
    def road_layer(self):
        return self._road_layer

    def point_layer(self):
        return self._point_layer

    def distances(self):
        return self._distances

    def points(self):
        points: List[Point] = []
        for distance_index_element in self._distances.values():
            points.append(distance_index_element.point)
        return sorted(points, key=lambda x: x.id())

    def get_closest_road(self, point: Point):
        distance_element: IndexElement = self._distances[point.id()]
        closest_point_distance = distance_element.get_closest_road()
        closest_road = closest_point_distance.road
        return closest_road


    def get_distances_from_point(self, point_id):
        return self._distances[point_id]

    def get_roads_from_distance_index(self):
        distances = self.distances()
        roads = set()
        for distance_index_element in distances.values():
            point_distances = distance_index_element.distances_queue
            for distance in point_distances:
                roads.add(distance.road)
        return list(roads)

    def as_dict(self):
        tmp_dict = {}

        for point_id in self.distances():
            point_distances = self.distances()[point_id].distances_queue
            distances_array = []
            for distance in point_distances:
                distances_array.append([distance.road.id(), distance.distance])
            tmp_dict[point_id] = distances_array
        return tmp_dict