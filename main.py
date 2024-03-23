# custom modules
from gis import Project
from gis import Layer

from tmma.utils import get_path, load_distance_index
from tmma.distance_index.main import DistanceIndex
from tmma.preprocesing.buffer_tuner import BufferTuner

def main():
    project = Project()
    project.add_layer_from(
        file_path=get_path('portageroads_normalized_new.gpkg'),
        layer_name='portageroads_normalized_new'
    )
    project.add_layer_from(
        file_path=get_path('data_1140268103_10sec_1.gpkg'),
        layer_name='data_1140268103_10sec_1'
    )
    project.print_layers()

    road_layer = project.get_layer_by_name('portageroads_normalized_new')
    gps_layer = project.get_layer_by_name('data_1140268103_10sec_1')

    print(road_layer.units(), gps_layer.units())

    distance_index_file = load_distance_index('.distance_index.json')
    distance_index = DistanceIndex(
        road_layer=road_layer,
        gps_layer=gps_layer,
        distanceIndex=distance_index_file
    )
    buffer = BufferTuner(distance_index).get_buffer()
    distance_index.remove_roads_outside_buffer(buffer=buffer)
    project.save_distance_index(
        distance_index=distance_index.as_dict(),
        distance_index_path='.filtered_distance_index.json'
    )