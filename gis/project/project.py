from os import getenv

from qgis.core import (
    QgsProject,
    QgsVectorLayer
)

from gis.layers.layer.main import Layer

class Project:
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
