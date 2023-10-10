from qgis.core import *
import qgis.utils

def add_file_layer(file_path, layer_name):
    layer = load_file_layer(file_path, layer_name)
    if layer.isValid():
        QgsProject.instance().addMapLayer(layer)
    else:
        print('layer not valid')

def load_file_layer(file_path, layer_name):
    layer = file_path + '|layername=' + layer_name
    print('loading layer: ', layer)
    return QgsVectorLayer(layer, layer_name, "ogr")

def print_layers():
    print('-----------------------------------------')
    print('layers in project:')
    for layer in QgsProject.instance().mapLayers().values():
        print(layer.name())
    print('-----------------------------------------')

def get_layer_by_name(name):
    return QgsProject.instance().mapLayersByName(name)[0]

def get_object_count_in_layer(layer):
    return len(list(layer.getFeatures()))

def create_point(object, x_name='X', y_name='Y'):
    x, y = object[x_name], object[y_name]
    point_xy = QgsPointXY(x, y)
    return QgsGeometry.fromPointXY(point_xy)\

def create_buffer(point, radius, segments=5):
    return point.buffer(radius, segments)

# def create_layer_of_roads(roads):
#     layer = QgsVectorLayer("LineString", "roads", "memory")
#     pr = layer.dataProvider()
#     pr.addAttributes([QgsField("id", QVariant.Int)])
#     layer.updateFields()

#     for i, road in enumerate(roads):
#         f = QgsFeature()
#         f.setGeometry(road)
#         f.setAttributes([i])
#         pr.addFeature(f)
#     layer.updateExtents()
#     return layer