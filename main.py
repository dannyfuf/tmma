# custom modules
from gis.layers.layer.main import Layer
from gis.project.project import Project
from gis.layers.normalizer.main import Normalizer

from tmma.distance_index.distance_index import DistanceIndex
from tmma.utils import get_path
from tmma.preprocesing.buffer_tuner import BufferTuner

def main():
    project = Project()
    project.add_layer_from(
        file_path=get_path('portageroads_norm.gpkg'),
        layer_name='portageroads_norm'
    )
    project.add_layer_from(
        file_path=get_path('data_1140268103_10sec_1_norm.gpkg'),
        layer_name='data_1140268103_10sec_1_norm'
    )
    project.print_layers()

    road_layer = project.get_layer_by_name('portageroads_norm')
    points_layer = project.get_layer_by_name('data_1140268103_10sec_1_norm')

    print(road_layer.units(), points_layer.units())

    distance_index = DistanceIndex(
        road_layer=road_layer,
        points_layer=points_layer,
        distance_index_path='.data/.distance_index.json'
    )

    buffer_tuner = BufferTuner(distance_index)
    buffer_size = buffer_tuner.get_buffer()
    print('buffer size: ', buffer_size)

    distance_index.remove_roads_outside_buffer(buffer_size)
    distance_index.save_to('.data/.distance_index_filtered.json')

    norm_filtered_roads = distance_index.get_layer_of_current_roads()
    norm_filtered_roads.save_to(get_path('portageroads_cleaned.gpkg'))