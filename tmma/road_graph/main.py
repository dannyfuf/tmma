from typing import List
from gis import Layer
import networkx as nx
import matplotlib.pyplot as plt

from gis import Line, Point

class RoadGraph:
    _road_layer: Layer

    def __init__(self, road_layer: Layer):
        self._road_layer = road_layer
        self._build_graph()

    def graph(self):
        return self._graph

    def describe_graph(self):
        print(f'nodes: {len(self._graph.nodes())}')
        print(f'edges: {len(self._graph.edges())}')
        print(self._graph.nodes())
        print(self._graph.edges())

    def compute_route(self, start_node_id, end_node_id):
        try:
            route = nx.shortest_path(self._graph, start_node_id, end_node_id)
            return route
        except nx.NetworkXNoPath:
            return []

    def build_layer_from_route(self, route):
        features = []
        for route_id in route:
            feature = self._road_layer.get_feature_by_id(route_id)
            features.append(feature)
        layer = Layer().build(
            self._road_layer.type(),
            'route',
            self._road_layer.crs_name(),
            self._road_layer.fields(),
            features
        )
        return layer

    def compute_route_length(self, route: List[Line], start_point: Point, end_point: Point):
        route_lines = self._build_route_lines(route)
        if len(route) == 1:
            return self._compute_distance_only_one_road(route_lines[0], start_point, end_point)

        intersections = self._compute_roads_intersections(route_lines)
        points_in_route = [start_point]+ intersections + [end_point]
        total_distance = 0
        for route_idx in range(len(route_lines)):
            point1 = points_in_route[route_idx]
            point2 = points_in_route[route_idx + 1]
            distance = self._compute_distance_only_one_road(route_lines[route_idx], point1, point2)
            total_distance += distance

        return total_distance

    def _compute_distance_only_one_road(self, road, start_point, end_point):
        distance_to_end_point = road.length_to(end_point)
        distance_to_start_point = road.length_to(start_point)
        return abs(distance_to_end_point - distance_to_start_point)

    def _build_graph(self):
        edges = self._compute_edges()
        self._graph = nx.Graph()
        self._graph.add_edges_from(edges)

    def _compute_edges(self):
        edges = []
        for feature1 in self._road_layer.features():
            geometry1 = feature1.geometry()
            for feature2 in self._road_layer.features():
                geometry2 = feature2.geometry()
                if feature1 != feature2:
                    if self._are_connected(geometry1, geometry2):
                        edges.append((feature1['fid'], feature2['fid']))
        return edges

    def _are_connected(self, geometry1, geometry2):
        return geometry1.touches(geometry2) or geometry1.intersects(geometry2)

    def _build_route_lines(self, route):
        lines = []
        for road_id in route:
            lines.append(Line(self._road_layer.get_feature_by_id(road_id)))
        return lines

    def _compute_roads_intersections(self, roads: List[Line]):
        intersections = []
        for road_idx in range(len(roads) - 1):
            road1 = roads[road_idx]
            road2 = roads[road_idx + 1]
            intersections.append(road1.intersection(road2))
        return intersections
