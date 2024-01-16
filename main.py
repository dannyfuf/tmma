# custom modules
from gis.project.project import Project
from gis.layers.normalizer import Normalizer
from tmma.utils import get_path

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

    layer = project.get_layer_by_name('portageroads')
    normalizer = Normalizer(layer)
    normalizer.normalize()
    normalized_layer = normalizer.normalized_layer()
    # normalizer.save(get_path('portageroads_normalized_new.gpkg'))
    print(layer.units())
    print(normalized_layer.units())
