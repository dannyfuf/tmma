from typing import List
from qgis.core import (
    QgsVectorLayer,
    QgsVectorFileWriter,
    QgsExpression,
    QgsFeatureRequest,
    QgsFields,
    QgsFeature
)


class Handlers:
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
    
    def save_to(self, file_path: str):
        print(f'saving layer to {file_path}')
        QgsVectorFileWriter.writeAsVectorFormat(self.layer(), file_path, "utf-8", self.layer().crs(), "GPKG")

    def get_feature_by_id(self, fid: int):
        return self.query(f"fid = {fid}")[0]

    def query(self, query: str):
        expresion = QgsExpression(query) # example: "fid = 1"
        request = QgsFeatureRequest(expresion)
        return list(self.layer().getFeatures(request))
        
    def query_by_id(self, fid: int):
        expresion = QgsExpression(f"fid = {fid}")
        request = QgsFeatureRequest(expresion)
        return list(self.layer().getFeatures(request))[0]

    def start_editing(self):
        self.layer().startEditing()

    def set_fields(self, fields: QgsFields):
        self.layer().dataProvider().addAttributes(fields)
        self.layer().updateFields()

    def commit(self):
        self.layer().commitChanges()

    def points_order(self):
        if self.type() == 'MultiLineString':
            raise Exception('Method not supported for MultiLineString layers')

        request = QgsFeatureRequest().addOrderBy('Time')
        sorted_features = self.layer().getFeatures(request)
        return [feature['fid'] for feature in sorted_features]
    
    def get_mean_speed(self):
        if self.type() == 'MultiLineString':
            raise Exception('Method not supported for MultiLineString layers')
        
        if len(self.features()) == 0:
            return 0

        speeds = []
        for feature in self.features():
            speeds.append(feature['Speed'])

        return sum(speeds) / len(speeds)