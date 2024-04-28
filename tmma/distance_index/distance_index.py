from json import dump, load

from .distance_index_element import DistanceIndexElement
from gis.layers.layer.main import Layer
from gis.geometries.points import Point, Line
from gis.project.project import Project
from gis.layers.normalizer.main import Normalizer

class DistanceIndex:
    __distances: dict[DistanceIndexElement]
    __road_layer: Layer
    __points_layer: Layer
    __points_order: list[str]

    def __init__(self,
        road_layer: Layer,
        points_layer: Layer,
        distance_index_path: str = None
    ):
        self.__road_layer = road_layer
        self.__points_layer = points_layer
        if distance_index_path:
            distance_index = self.__load_from_file(distance_index_path)
            self.__distances = self.__build_distance_elements(distance_index)
        else:
            self.__distances = self.__build_distance_index_from_layers()

    def __load_from_file(self, distance_index_path: str):
        with open(distance_index_path, 'r') as f:
            distance_index_json = load(f)
        print('loaded distance index from: ', distance_index_path)
        return distance_index_json

    def __build_distance_elements(self, distance_index):
        tmp_distance_index = {}
        for point in distance_index:
            tmp_distance_index[point] = DistanceIndexElement(point, distance_index[point])
        return tmp_distance_index
    
    def __build_distance_index_from_layers(self):
        print('building distance index from layers')
        tmp_distance_index = {}
        points = [Point(point) for point in self.__points_layer.features()]
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

    def __get_road_ids(self):
        road_ids = []
        for point_id in self.distances():
            point_distances = self.distances()[point_id].distances_queue
            for distance in point_distances:
                road_ids.append(distance.road_id)
        return list(set(road_ids))

    def save_to(
            self,
            distance_index_path: str = '.data/.distance_index.json'
        ):
        distance_index = self.as_dict()
        with open(distance_index_path, 'w') as f:
            dump(distance_index, f)
        print('saved distance index to: ', distance_index_path)

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
    
    def get_layer_of_current_roads(self):
        road_ids = self.__get_road_ids()
        filtered_features = []
        for road_id in road_ids:
            road = self.__road_layer.get_feature_by_id(road_id)
            filtered_features.append(road)

        layer_name = f'{self.__road_layer.name()}_cleaned'
        filtered_road = Layer().build(
            layer_type=self.__road_layer.type(),
            layer_name=layer_name,
            layer_crs=self.__road_layer.crs(),
            fields=self.__road_layer.fields(),
            features=filtered_features
        )
        normalizer = Normalizer()
        norm_filtered_road = normalizer.normalize(filtered_road)
        return norm_filtered_road