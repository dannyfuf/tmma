from qgis.core import QgsFeature

from geometry.layers import search_feature_by

def get_feature(layer, fid):
    return search_feature_by(layer, f"fid = {fid}")[0]

class Distance:
    road_id: str
    distance: float

    def __init__(self, road_id, distance):
        self.road_id = road_id
        self.distance = distance

class DistanceIndexElement:
    point_id: str
    distances: list[Distance]
    distances_queue: list[Distance]
    current_road: Distance

    def __init__(self, point, distances):
        self.point_id = point
        self.distances_queue = self._build_distances(distances)
        self.snapped_road = None
        self.current_road = None

    def _build_distances(self, distances):
        tmp_distances = []
        for distance in distances:
            tmp_distances.append(Distance(distance[0], distance[1]))
        return tmp_distances

    def point(self):
        return 

    def get_next_candidate_road(self):
        if len(self.distances_queue) == 0:
            self.current_road = None
            return None
        self.current_road = self.distances_queue.pop(0)
        return str(self.current_road.road_id)

class DistanceIndex:
    __distances: dict[DistanceIndexElement]
    __road_layer: QgsFeature
    __gps_layer: QgsFeature
    __points_order: list[str]
    __current_point: str
    __current_point_idx: int
    __current_road: QgsFeature

    def __init__(self, distanceIndex, points_order, road_layer, gps_layer):
        self.__distances = self._build_distance_index(distanceIndex)
        self.__current_point = None
        self.__points_order = points_order
        self.__road_layer = road_layer
        self.__current_point_idx = -1
        self.__gps_layer = gps_layer
        self.__current_road = None

    def _build_distance_index(self, distance_index):
        tmp_distance_index = {}
        for point in distance_index:
            tmp_distance_index[point] = DistanceIndexElement(point, distance_index[point])
        return tmp_distance_index
    
    def current_point(self):
        return get_feature(self.__gps_layer, self.__current_point)
    
    def current_point_id(self):
        return self.__current_point

    def set_next_point(self):
        if self.__current_point_idx + 1 >= len(self.__points_order):
            self.__current_point = None
            return False
        self.__current_point_idx += 1
        self.__current_point = str(self.__points_order[self.__current_point_idx])
        return True

    def set_next_candidate_road(self):
        if self.__current_point is None:
            return False

        fid_road = self.__distances[self.__current_point].get_next_candidate_road()
        if fid_road is None:
            self.__current_road = None
            return False
        self.__current_road = fid_road
        return True
    
    def get_next_candidate_road(self):
        self.set_next_candidate_road()
        return self.candidate_road()

    def candidate_road(self):
        return get_feature(self.__road_layer, self.__current_road)
    
    def road_candidate_id(self):
        return self.__current_road

