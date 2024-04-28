# custom modules
from gis.layers.layer.main import Layer
from gis.project.project import Project
from gis.layers.normalizer.main import Normalizer

from tmma.distance_index.distance_index import DistanceIndex
from tmma.preprocesing.main import Preprocessing
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

    preprocessing = Preprocessing(
        road_layer=road_layer,
        points_layer=points_layer,
        distance_index=distance_index
    )
    preprocessing.run()
    buffer_size = preprocessing.buffer_size
    print(f'buffer size: {buffer_size}')