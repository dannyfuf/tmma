# custom modules
from gis.project.project import Project
from gis.layers.normalizer import Normalizer

from tmma.utils import get_path
from tmma.distance_index.distance_index import DistanceIndex

from tmma.utils import load_distance_index

def main():
    project = Project()
    project.add_layer_from(
        file_path=get_path('portageroads.gpkg'),
        layer_name='portageroads'
    )
    project.add_layer_from(
        file_path=get_path('data_1140268103_10sec_1.gpkg'),
        layer_name='data_1140268103_10sec_1'
    )
    project.print_layers()

    road_layer = project.get_layer_by_name('portageroads')
    gps_layer = project.get_layer_by_name('data_1140268103_10sec_1')

    distance_index = DistanceIndex(road_layer=road_layer, gps_layer=gps_layer)