from qgis.core import QgsFeature

from .distance_index_element import DistanceIndexElement
from gis.layers.layers import Layer
from gis.geometries.points import Point, Line
from gis.project.project import Project

class DistanceIndex:
    __distances: dict[DistanceIndexElement]
    __road_layer: Layer
    __gps_layer: Layer
    __points_order: list[str]
    __current_point: DistanceIndexElement
    __current_candidate_road: QgsFeature

    def __init__(self, road_layer: Layer, gps_layer: Layer, distanceIndex: dict[str, list[tuple[str, float]]] = None):
        self.__road_layer = road_layer
        self.__gps_layer = gps_layer
        self.__points_order = self.__gps_layer.points_order()
        self.__current_point = None
        self.__current_candidate_road = None
        if distanceIndex:
            self.__distances = self.__build_distance_elements(distanceIndex)
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

        project = Project()
        project.save_distance_index(tmp_distance_index)
        distance_index = self.__build_distance_elements(tmp_distance_index)
        return distance_index


    def current_point(self):
        query = f"fid = {self.__current_point.point_id}"
        return self.__gps_layer.query(query)[0]
    
    def current_point_id(self):
        return self.__current_point.point_id

    def set_next_point(self):
        if len(self.__points_order) == 0:
            self.__current_point = None
            return False

        idx = str(self.__points_order.pop(0))
        self.__current_point = self.__distances[idx]
        return True

    def set_next_candidate_road(self):
        if self.__current_point is None:
            return False

        fid_road = self.__current_point.get_next_candidate_road_id()
        if fid_road is None:
            self.__current_candidate_road = None
            return False
        self.__current_candidate_road = self.__road_layer.query(f"fid = {fid_road}")[0]
        return True
    
    def get_next_candidate_road(self):
        self.set_next_candidate_road()
        return self.__current_candidate_road
    
    def road_candidate_id(self):
        if self.__current_candidate_road is None:
            return None
        return self.__current_candidate_road['fid']
    
    def current_point_id(self):
        if self.__current_point is None:
            return None
        return self.__current_point.point_id

