
class GetPointsWithoutSnap:
    def __init__(self, route, points):
        self.route = route
        self.points = points

    def run(self):
        points_without_snap = []
        snapped_points = self._snapped_points()
        for point in self.points:
            if point.id() not in snapped_points:
                points_without_snap.append(point)

        return points_without_snap

    def _snapped_points(self):
        return [snap.point.id() for snap in self.route]