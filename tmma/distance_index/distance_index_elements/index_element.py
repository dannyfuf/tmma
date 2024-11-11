from gis import Point
from .distance import Distance

class IndexElement:
    point: Point
    distances_queue: list[Distance]
    frozen_distances: list[Distance]

    def __init__(self, point, road_distances):
        self.point = point
        self.distances_queue = road_distances
        self.frozen_distances = road_distances

    def get_closest_road(self):
        closest_road = self.distances_queue[0]
        self.distances_queue.pop(0)
        return closest_road