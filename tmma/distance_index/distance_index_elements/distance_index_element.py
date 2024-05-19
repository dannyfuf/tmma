from gis.geometries.points import Point
from .distance import Distance

class DistanceIndexElement:
    point_id: str
    point: Point
    distances_queue: list[Distance]

    def __init__(self, point, road_distances):
        self.point = point
        self.point_id = point.id()
        self.distances_queue = road_distances
