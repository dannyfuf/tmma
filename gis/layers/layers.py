from typing import List
from qgis.core import (
    QgsVectorLayer,
    QgsVectorFileWriter,
    QgsExpression,
    QgsFeatureRequest,
    QgsWkbTypes,
    QgsFields,
    QgsFeature
)

class Layer:
    __layer: QgsVectorLayer = None

    def __init__(self, layer: QgsVectorLayer = None):
        self.__layer = layer

    def new(self, layer_type: str, layer_name: str, layer_crs: str):
        self.__layer = QgsVectorLayer(f"{layer_type}?crs={layer_crs}", layer_name, "memory")
        return self
    
    def build(
            self,
            layer_type: str,
            layer_name: str,
            layer_crs: str,
            fields: QgsFields,
            features: List[QgsFeature]
        ):
        self.new(layer_type, layer_name, layer_crs)
        self.start_editing()
        self.set_fields(fields)

        for feature in features:
            converted_feature = QgsFeature()
            converted_feature.setGeometry(feature.geometry())
            converted_feature.setAttributes(feature.attributes())
            self.add_feature(converted_feature)

        self.commit()
        return self
    
    def layer(self):
        return self.__layer

    def name(self):
        return self.layer().name()

    def crs(self):
        return self.layer().crs()
    
    def crs_name(self):
        return self.layer().crs().authid()

    def units(self):
        return self.layer().crs().mapUnits()
    
    def fields(self):
        return self.layer().fields()
    
    def field_names(self):
        return list(map(lambda field: field.name(), self.fields()))
    
    def features(self):
        return self.layer().getFeatures()

    def save_to(self, file_path: str):
        QgsVectorFileWriter.writeAsVectorFormat(self.layer(), file_path, "utf-8", self.layer().crs(), "GPKG")

    def query(self, query: str):
        expresion = QgsExpression(query) # example: "fid = 1"
        request = QgsFeatureRequest(expresion)
        return list(self.layer().getFeatures(request))

    def type(self):
        layer_type = self.layer().wkbType()
        if layer_type == QgsWkbTypes.MultiLineString:
            return 'MultiLineString'
        elif layer_type == QgsWkbTypes.Point:
            return 'MultiPoint'
        elif layer_type == QgsWkbTypes.MultiPoint:
            return 'MultiPoint'
        else:
            raise Exception('Layer type not supported')
        
    def start_editing(self):
        self.layer().startEditing()

    def set_fields(self, fields: QgsFields):
        self.layer().dataProvider().addAttributes(fields)
        self.layer().updateFields()

    def add_feature(self, feature):
        self.layer().addFeature(feature)

    def commit(self):
        self.layer().commitChanges()

    def points_order(self):
        if self.type() == 'MultiLineString':
            raise Exception('Method not supported for MultiLineString layers')

        request = QgsFeatureRequest().addOrderBy('Time')
        sorted_features = self.layer().getFeatures(request)
        return [feature['fid'] for feature in sorted_features]
        