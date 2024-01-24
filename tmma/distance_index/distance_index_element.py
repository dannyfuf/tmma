from .distance import Distance

class DistanceIndexElement:
    point_id: str
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

    def get_next_candidate_road_id(self):
        if len(self.distances_queue) == 0:
            self.current_road = None
            return None
        self.current_road = self.distances_queue.pop(0)
        return str(self.current_road.road_id)