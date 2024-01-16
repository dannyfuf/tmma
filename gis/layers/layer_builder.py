from typing import List, Any, TypedDict

from qgis.core import *

# custom modules
from geometry.points import create_point
from geometry.layers import create_vector_layer, get_layer_crs
from geometry.lines import create_line

class LayerFields(TypedDict):
    name: str
    type: Any

class LayerConfig(TypedDict):
    layer_name: str
    layer_type: str
    layer_crs: str
    layer_fields: List[LayerFields]

def build_point_layer(
    layer_features: List[QgsFeature],
    layer_config: LayerConfig
):
    vector_layer = create_vector_layer(
        layer_name=layer_config['layer_name'],
        layer_type=layer_config['layer_type'],
        layer_crs=layer_config['layer_crs']
    )
    layer_provider = vector_layer.dataProvider()

    attributes = [QgsField(field['name'], field['type']) for field in layer_config['layer_fields']]
    layer_provider.addAttributes(attributes)
    vector_layer.updateFields()

    features = []
    for object in layer_features:
        new_feature = QgsFeature()
        point = create_point(object)
        new_feature.setGeometry(point)

        attr_ = [object[field['name']] for field in layer_config['layer_fields']]
        new_feature.setAttributes(attr_)
        features.append(new_feature)

    layer_provider.addFeatures(features)
    
    return vector_layer


def build_line_layer(
    layer_features: List[QgsFeature],
    layer_config: LayerConfig
):
    vector_layer = create_vector_layer(
        layer_name=layer_config['layer_name'],
        layer_type=layer_config['layer_type'],
        layer_crs=layer_config['layer_crs']
    )
    layer_provider = vector_layer.dataProvider()

    attributes = [QgsField(field['name'], field['type']) for field in layer_config['layer_fields']]
    layer_provider.addAttributes(attributes)
    vector_layer.updateFields()

    features = []
    for object in layer_features:
        new_feature = QgsFeature()
        line = create_line(object)
        new_feature.setGeometry(line)

        attr_ = [object[field['name']] for field in layer_config['layer_fields']]
        new_feature.setAttributes(attr_)
        features.append(new_feature)

    layer_provider.addFeatures(features)
    
    return vector_layer

# convert a layer with lines to a layer with 
def normalize_line_layer(
    layer: QgsVectorLayer,
):
    standard_crs_name = 'EPSG:32633'

    original_features = layer.getFeatures()
    original_crs = layer.crs()

    standard_crs = QgsCoordinateReferenceSystem(standard_crs_name)
    transformer = QgsCoordinateTransform(original_crs, standard_crs, QgsProject.instance())

    converted_layer = QgsVectorLayer(f'MultiLineString?crs={standard_crs_name}', layer.name(), 'memory')
    converted_layer.startEditing()

    for feature in original_features:
        original_geometry = feature.geometry()
        converted_geometry = QgsGeometry(original_geometry)
        converted_geometry.transform(transformer)

        converted_feature = QgsFeature()
        converted_feature.setGeometry(converted_geometry)
        converted_layer.addFeature(converted_feature)

    converted_layer.commitChanges()
    return converted_layer

def normalize_point_layer(
    layer: QgsVectorLayer,
):
    standard_crs_name = 'EPSG:32633'

    original_features = layer.getFeatures()
    original_crs = layer.crs()

    standard_crs = QgsCoordinateReferenceSystem(standard_crs_name)
    transformer = QgsCoordinateTransform(original_crs, standard_crs, QgsProject.instance())

    converted_layer = QgsVectorLayer(f'MultiPoint?crs={standard_crs_name}', layer.name(), 'memory')
    converted_layer.startEditing()

    for feature in original_features:
        original_geometry = feature.geometry()
        converted_geometry = QgsGeometry(original_geometry)
        converted_geometry.transform(transformer)

        converted_feature = QgsFeature()
        converted_feature.setGeometry(converted_geometry)
        converted_layer.addFeature(converted_feature)

    converted_layer.commitChanges()
    return converted_layer