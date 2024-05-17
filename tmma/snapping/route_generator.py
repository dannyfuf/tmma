from qgis.analysis import QgsVectorLayerDirector, QgsGraphBuilder, QgsGraphAnalyzer
from qgis.core import QgsGeometry

from gis.geometries.lines import Line
from gis.geometries.points import Point
from gis.layers.layer.main import Layer


class RouteGenerator:
    __road_layers: Layer = None
    __graph = None
    __tied_points = None

    def __init__(self, road_layers: Layer):
        self.__road_layers = road_layers
    
    def road_layers(self):
        return self.__road_layers

    def graph(self):
        return self.__graph
    
    def tied_points(self):
        return self.__tied_points

    def startPointId(self):
        return self.graph().findVertex(self.tied_points()[0])
    
    def endPointId(self):
        return self.graph().findVertex(self.tied_points()[1])

    def generate_route(self, start_point: Point, end_point: Point):
        self.build_graph(start_point, end_point)
        computed_route = self.compute_route()
        roads_route = []
        for point in computed_route:
            point_geometry = QgsGeometry.fromPointXY(point)
            for road in self.road_layers().features():
                if road.geometry().intersects(point_geometry):
                    if road not in roads_route:
                        roads_route.append(road)

        return [Line(road) for road in roads_route][::-1] # creo que quedan al reves. No estoy seguro de pq

    def compute_route(self):
        startId = self.startPointId()
        endId = self.endPointId()
        (tree, cost) = QgsGraphAnalyzer.dijkstra(self.graph(), startId, 0)

        route = [self.graph().vertex(endId).point()]
        while endId != startId:
            edge = self.graph().edge(tree[endId])
            endId = edge.fromVertex()
            route.insert(0, self.graph().vertex(endId).point())
        
        return route

    def build_graph(self, start_point: Point, end_point: Point):
        start_point_xy = start_point.geometry().asPoint()
        end_point_xy = end_point.geometry().asPoint()

        director = QgsVectorLayerDirector(
            self.road_layers().layer(),
            -1,
            '',
            '',
            '', 
            QgsVectorLayerDirector.DirectionBoth
        )
        builder = QgsGraphBuilder(self.road_layers().layer().crs())
        tiedPoints = director.makeGraph(builder, [start_point_xy, end_point_xy])
        graph = builder.graph()
        self.__graph = graph
        self.__tied_points = tiedPoints

    def calculate_route_lenght(
        self,
        route: list[Line],
        start_point: Point,
        end_point: Point
    ):
        initial_road_full_lenght = route[0].length()
        initial_road_lenght = initial_road_full_lenght - route[0].length_to(start_point)
        
        end_road_lenght = 0
        if len(route) == 1:
            end_road_lenght = route[0].length_to(end_point) - initial_road_lenght
        else:
            end_road_lenght = route[-1].length_to(end_point)

        total_distance = initial_road_lenght + end_road_lenght
        for road in route[1:-1]:
            total_distance += road.length()

        return total_distance