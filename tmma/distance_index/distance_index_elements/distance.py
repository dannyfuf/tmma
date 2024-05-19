from gis.geometries.lines import Line


class Distance:
    road: Line
    distance: float

    def __init__(self, road, distance):
        self.road = road
        self.distance = distance