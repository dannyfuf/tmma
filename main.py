# custom modules
from gis.project.project import Project
# from gis.layers.normalizer.main import Normalizer

from tmma.utils import get_path, load_distance_index
from tmma.distance_index.distance_index import DistanceIndex

def main():
    project = Project()
    project.add_layer_from(
        file_path=get_path('portageroads_normalized.gpkg'),
        layer_name='portageroads_normalized'
    )
    project.add_layer_from(
        file_path=get_path('data_1140268103_10sec_1.gpkg'),
        layer_name='data_1140268103_10sec_1'
    )
    project.print_layers()

    road_layer = project.get_layer_by_name('portageroads_normalized')
    gps_layer = project.get_layer_by_name('data_1140268103_10sec_1')

    print(road_layer.units(), gps_layer.units())

    # distance_index = DistanceIndex(
    #     road_layer=road_layer,
    #     gps_layer=gps_layer,
    # )
    # buffer = BufferTuner(distance_index).get_buffer()
    # distance_index.remove_roads_outside_buffer(buffer=buffer)
    # project.save_distance_index(
    #     distance_index=distance_index.as_dict(),
    #     distance_index_path='.filtered_distance_index.json'
    # )