class Accessors:
    def road_layer(self):
        return self._road_layer
    
    def points_layer(self):
        return self._points_layer

    def distances(self):
        return self._distances

    def get_distances_from_point(self, point_id):
        return self._distances[point_id].distances_queue

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
                distances_array.append([distance.road_id, distance.distance])
            tmp_dict[point_id] = distances_array
        return tmp_dict