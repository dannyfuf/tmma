from json import dump, load

from gis import Line, Point, Layer
from ..distance_index_elements import DistanceIndexElement, Distance


class Handlers:
    def save_to(
            self,
            distance_index_path: str = '.data/.distance_index.json'
        ):
        distance_index = self.as_dict()
        with open(distance_index_path, 'w') as f:
            dump(distance_index, f)
        print('Saved distance index to: ', distance_index_path)

    def remove_roads_outside_buffer(self, buffer):
        for point_id in self.distances():
            point_distances = self.distances()[point_id]
            number_of_roads = len(point_distances.distances_queue)
            for i in range(number_of_roads):
                road = point_distances.distances_queue[i]
                if road.distance > buffer:
                    point_distances.distances_queue = point_distances.distances_queue[:i]
                    break
    
    def build_road_layer_from_distance_index(self):
        print('Building road layer from distance index')
        roads = self.get_roads_from_distance_index()
        roads_features = [road.feature() for road in roads]
        road_layer = Layer().build(
            layer_type=self._road_layer.type(),
            layer_name=f'{self._road_layer.name()}_current',
            layer_crs=self._road_layer.crs_name(),
            fields=self._road_layer.fields(),
            features=roads_features
        )
        return road_layer


    def _load_from_file(self, distance_index_path: str):
        with open(distance_index_path, 'r') as f:
            distance_index_json = load(f)
        print('Loaded distance index from: ', distance_index_path)
        return distance_index_json

    def _build_distance_elements(self, distance_index):
        tmp_distance_index = {}
        for point_id in distance_index:
            point = Point(self._point_layer.get_feature_by_id(point_id))
            point_distances = self._build_distances(distance_index[point_id])
            tmp_distance_index[point_id] = DistanceIndexElement(point, point_distances)
        return tmp_distance_index
    
    def _build_distances(self, road_distances):
        tmp_distances = []
        for road_id, road_distance in road_distances:
            road = Line(self._road_layer.get_feature_by_id(road_id))
            tmp_distances.append(Distance(road, road_distance))
        return tmp_distances

    def _build_distance_index_from_layers(self):
        print('Building distance index from layers')
        tmp_distance_index = {}
        points = [Point(point) for point in self._point_layer.features()]
        roads = [Line(road) for road in self._road_layer.features()]
        for point in points:
            road_distances = []
            for road in roads:
                distance = point.distance_to(road)
                road_distances.append((road.id(), distance))
            road_distances.sort(key=lambda x: x[1])
            tmp_distance_index[point.id()] = road_distances

        distance_index = self._build_distance_elements(tmp_distance_index)
        return distance_index
