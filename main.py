# custom modules
from gis.geometries.lines import Line
from gis.geometries.points import Point
from gis.layers.layer.main import Layer
from gis.project.project import Project
# from gis.layers.normalizer.main import Normalizer

# from tmma.distance_index.distance_index import DistanceIndex
# from tmma.preprocesing.main import Preprocessing
# from tmma.snapping.route_graph import RoutesGraph
from tmma.snapping.route_generator import RouteGenerator
from tmma.utils import get_path
# from tmma.preprocesing.buffer_tuner import BufferTuner

def main():
    project = Project()
    project.add_layer_from(
        file_path=get_path('test_roads.gpkg'),
        layer_name='tmp_roads'
    )
    project.add_layer_from(
        file_path=get_path('test_points.gpkg'),
        layer_name='test_points'
    )
    project.print_layers()

    road_layer = project.get_layer_by_name('tmp_roads')
    points_layer = project.get_layer_by_name('test_points')

    print(road_layer.units(), points_layer.units())

    point1 = Point(points_layer.features()[0])
    point2 = Point(points_layer.features()[1])
    road1 = Line(road_layer.features()[0])
    road2 = Line(road_layer.features()[1])

    proj1 = road1.project(point1)
    proj2 = road2.project(point2)

    route_generator = RouteGenerator(road_layer)
    route = route_generator.generate_route(proj1, proj2)
    route_length = route_generator.calculate_route_lenght(route, proj1, proj2)
    print(route_length)

    Layer().build(
        road_layer.type(),
        'route_roads',
        road_layer.crs_name(),
        road_layer.fields(),
        [road.feature() for road in route]
    ).save_to(get_path('tmp_path_roads.gpkg'))