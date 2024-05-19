from gis.geometries.lines import Line


class Distance:
    road: Line
    road_id: str
    distance: float

    def __init__(self, road, distance):
        self.road = road
        self.road_id = road.id()
        self.distance = distance