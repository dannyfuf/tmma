from gis import Layer

class BuildSnappedPointsLayer:
    def __init__(self, route, point_layer):
        self._route = route
        self._point_layer = point_layer

    def run(self):
        snapped_points = [snap.projected_point.feature() for snap in self._route]

        return Layer().build(
            self._point_layer.type(),
            'snapped_points',
            self._point_layer.crs_name(),
            self._point_layer.fields(),
            snapped_points
        )