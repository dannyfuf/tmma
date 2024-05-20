from gis import Point, Line


class Snap:
    def __init__(self, point, road, projected_point):
        self.point: Point = point
        self.road: Line = road
        self.projected_point: Point = projected_point
