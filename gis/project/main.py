from os import getenv
from json import dump, load

from qgis.core import (
    QgsProject,
    QgsVectorLayer
)

from .. import Layer

class Project:
    __distance_index: dict = None

    def get_path(self, filename):
        return f'{getenv("DATA_PATH")}/{filename}'

    def add_layer_from(
        self,
        file_path: str,
        layer_name: str
    ):
        layer = self.read_layer_from_file(file_path, layer_name)
        if layer.isValid():
            QgsProject.instance().addMapLayer(layer)
        else:
            print('layer not valid')

    def read_layer_from_file(
        self,
        file_path: str,
        layer_name: str
    ):
        layer = file_path + '|layername=' + layer_name
        print('loading layer: ', layer)
        return QgsVectorLayer(layer, layer_name, "ogr")

    def get_layer_by_name(self, layer_name: str):
        return Layer(QgsProject.instance().mapLayersByName(layer_name)[0])
    
    def print_layers(self):
        print('-----------------------------------------')
        print('         layers in project:')
        print('-----------------------------------------')
        for layer in QgsProject.instance().mapLayers().values():
            print(layer.name())
        print('-----------------------------------------')

    def save_distance_index(
            self,
            distance_index: dict,
            distance_index_path: str = '.distance_index.json'
        ):
        with open(distance_index_path, 'w') as f:
            dump(distance_index, f)
        print('saved distance index to: ', distance_index_path)

    def load_distance_index(self):
        distance_index_path = '.distance_index.json'
        with open(distance_index_path, 'r') as f:
            distance_index = load(f)
        print('loaded distance index from: ', distance_index_path)
        self.__distance_index = distance_index
        return self.__distance_index