from qgis.core import *

def add_file_layer(
    file_path: str,
    layer_name: str
):
    layer = load_file_layer(file_path, layer_name)
    if layer.isValid():
        QgsProject.instance().addMapLayer(layer)
    else:
        print('layer not valid')

def load_file_layer(
    file_path: str,
    layer_name: str
):
    layer = file_path + '|layername=' + layer_name
    print('loading layer: ', layer)
    return QgsVectorLayer(layer, layer_name, "ogr")

def print_layers():
    print('-----------------------------------------')
    print('         layers in project:')
    print('-----------------------------------------')
    for layer in QgsProject.instance().mapLayers().values():
        print(layer.name())
    print('-----------------------------------------')