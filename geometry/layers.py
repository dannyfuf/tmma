from qgis.core import *

# ------------------------------------------------------------
#                         BUILDERS
# ------------------------------------------------------------

def create_vector_layer(
    layer_name: str,
    layer_type: str,
    layer_crs: str
):
    return QgsVectorLayer(f"{layer_type}?crs={layer_crs}", layer_name, "memory")

def save_layer_to_file(
    layer: QgsVectorLayer,
    file_path: str
):
    QgsVectorFileWriter.writeAsVectorFormat(layer, file_path, "utf-8", layer.crs(), "GPKG")

# ------------------------------------------------------------
#                         GETTERS
# ------------------------------------------------------------

def get_layer_by_name(name: str):
    return QgsProject.instance().mapLayersByName(name)[0]

def get_object_count_in_layer(layer: QgsVectorLayer):
    return len(list(layer.getFeatures()))

def get_layer_fields(layer: QgsVectorLayer):
    return layer.fields().names()

def get_layer_features(layer: QgsVectorLayer):
    return layer.getFeatures()

def get_layer_crs(layer: QgsVectorLayer):
    return layer.crs().authid()

def search_feature_by(layer: QgsVectorLayer, query: str):
    expresion = QgsExpression(query)
    request = QgsFeatureRequest(expresion)
    return list(layer.getFeatures(request))