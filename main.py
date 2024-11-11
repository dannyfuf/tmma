from qgis.core import QgsFeature
import time

# custom modules
from gis.project.project import Project # file project.py is different from project/main.py --> fix this
from tmma import DistanceIndex, TMMA
from tmma.road_graph.main import RoadGraph
from utils import get_path

def main():
    project = Project()
    road_layer = project.add_layer_from(
        file_path=get_path('portageroads_cleaned.gpkg'),
        layer_name='portageroads_cleaned'
    )
    points_layer = project.add_layer_from(
        file_path=get_path('data_1140268103_10sec_1_norm.gpkg'),
        layer_name='data_1140268103_10sec_1_norm'
    )

    project.print_layers()
    print(road_layer.units(), points_layer.units())
    print(road_layer.crs_name(), points_layer.crs_name())
    print(points_layer.type(), road_layer.type())

    distance_index = DistanceIndex(road_layer, points_layer)
    distance_index.save_to('.data/.distance_index.json')
    tmma = TMMA(distance_index, 10)
    tmma.run()
    snapped_roads_layer = tmma.build_snapped_roads_layer()
    snapped_points_layer = tmma.build_snapped_points_layer()

    timestamp = int(time.time())
    snapped_roads_layer.save_to(get_path(f'{timestamp}_snapped_roads_mean.gpkg'))
    snapped_points_layer.save_to(get_path(f'{timestamp}_snapped_points_mean.gpkg'))
