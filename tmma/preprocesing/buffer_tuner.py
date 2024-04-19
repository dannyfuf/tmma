from ..distance_index.distance_index import DistanceIndex

class BufferTuner:
    distance_index: DistanceIndex

    def __init__(self, distance_index: DistanceIndex):
        self.distance_index = distance_index

    def get_buffer(self):
        buffer_size = 0

        nearest_road_by_point = []
        for point in self.distance_index.distances().values():
            nearest_road = point.distances_queue[0].distance
            nearest_road_by_point.append(nearest_road)

        buffer_size = max(nearest_road_by_point)
        return buffer_size