from gis import Layer

class BuildSnappedRoadsLayer:
    def __init__(self, route, road_layer):
        self._route = route
        self._road_layer = road_layer

    def run(self):
        roads = list(set([snap.road.feature() for snap in self._route]))
        return Layer().build(
            self._road_layer.type(),
            'snapped_roads',
            self._road_layer.crs_name(),
            self._road_layer.fields(),
            roads
        )