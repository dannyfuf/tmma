from qgis.core import QgsFeature

from .distance_index_element import DistanceIndexElement
from gis.layers.layer.main import Layer
from gis.geometries.points import Point, Line
from gis.project.project import Project

class DistanceIndex:
    __distances: dict[DistanceIndexElement]
    __road_layer: Layer
    __gps_layer: Layer
    __points_order: list[str]

    def __init__(self, road_layer: Layer, gps_layer: Layer, distance_index: dict[str, list[tuple[str, float]]] = None):
        self.__road_layer = road_layer
        self.__gps_layer = gps_layer
        if distance_index:
            self.__distances = self.__build_distance_elements(distance_index)
        else:
            self.__distances = self.__build_distance_index_from_layers()

    def __build_distance_elements(self, distance_index):
        tmp_distance_index = {}
        for point in distance_index:
            tmp_distance_index[point] = DistanceIndexElement(point, distance_index[point])
        return tmp_distance_index
    
    def __build_distance_index_from_layers(self):
        tmp_distance_index = {}
        points = [Point(point) for point in self.__gps_layer.features()]
        for point in points:
            road_distances = []
            roads = [Line(road) for road in self.__road_layer.features()]
            for road in roads:
                distance = point.distance_to(road)
                road_distances.append((road.id(), distance))
            road_distances.sort(key=lambda x: x[1])
            tmp_distance_index[point.id()] = road_distances

        distance_index = self.__build_distance_elements(tmp_distance_index)
        return distance_index
    
    def distances(self):
        return self.__distances

    def get_distances_from_point(self, point_id):
        return self.__distances[point_id].distances_queue

    def remove_roads_outside_buffer(self, buffer):
        for point_id in self.distances():
            point_distances = self.distances()[point_id]
            number_of_roads = len(point_distances.distances_queue)
            for i in range(number_of_roads):
                road = point_distances.distances_queue[i]
                if road.distance > buffer:
                    point_distances.distances_queue = point_distances.distances_queue[:i]
                    break
    
    def as_dict(self):
        tmp_dict = {}

        for point_id in self.distances():
            point_distances = self.distances()[point_id].distances_queue
            distances_array = []
            for distance in point_distances:
                distances_array.append([distance.road_id, distance.distance])
            tmp_dict[point_id] = distances_array
        return tmp_dict
