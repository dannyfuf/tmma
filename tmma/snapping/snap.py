from gis import Point, Line


class Snap:
    def __init__(self, point, road, projected_point, route_to_last_snap):
        self.point: Point = point
        self.road: Line = road
        self.projected_point: Point = projected_point
        self.route_to_last_snap = route_to_last_snap

    def __repr__(self):
        return f''''
        Snap:
            point: {self.point}
            road: {self.road}
            projected_point: {self.projected_point}
            route_to_last_snap: {self.route_to_last_snap}
        '''