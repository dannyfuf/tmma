from tmma import Snap

class GetResultRoads:
    def __init__(self, route: list[Snap]):
        self.route = route

    def run(self):
        result_roads = self._get_flattened_result_roads()
        result_roads_list = self._select_unique(result_roads)
        return result_roads_list

    def _get_flattened_result_roads(self):
        result_roads = set()
        for snap in self.route:
            if snap.route_to_last_snap is not None:
                for road in snap.route_to_last_snap:
                    result_roads.add(road)
        return result_roads

    def _select_unique(self, unique_roads):
        unique_roads = list(unique_roads)
        unique_roads.sort()
        return unique_roads