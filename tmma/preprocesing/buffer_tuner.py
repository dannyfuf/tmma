from ..distance_index.main import DistanceIndex

class BufferTuner:
    distance_index: DistanceIndex

    def __init__(self, distance_index: DistanceIndex):
        self.distance_index = distance_index

    def get_buffer(self):
        buffer_size = 0

        for point_id in self.distance_index.distances():
            distance_to_nearest_road = self.distance_index.distances()[point_id].distances_queue[0].distance

            if distance_to_nearest_road > buffer_size:
                buffer_size = distance_to_nearest_road
        
        return buffer_size