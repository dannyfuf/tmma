from qgis.core import (
    QgsCoordinateTransform,
    QgsGeometry,
    QgsFeature,
)

from ..layer import Layer

class Handlers:
    def build_crs_transformer(self, crs_from, context):
        return QgsCoordinateTransform(
            crs_from,
            self.crs_to(),
            context
        )

    def normalize(self):
        fields = self.layer().fields()
        normalized_layer = Layer().new(
            layer_type=self.layer().type(),
            layer_name=self.layer().name(),
            layer_crs=self.default_crs()
        )

        normalized_layer.start_editing()
        normalized_layer.set_fields(fields)

        for feature in self.layer().features():
            original_geometry = feature.geometry()
            converted_geometry = QgsGeometry(original_geometry)
            converted_geometry.transform(self.transformer())

            converted_feature = QgsFeature()
            converted_feature.setGeometry(converted_geometry)
            converted_feature.setAttributes(feature.attributes())
            normalized_layer.add_feature(converted_feature)

        normalized_layer.commit()
        self.__normalized_layer = normalized_layer
    
    def save(self, path: str):
        self.normalized_layer().save_to(path)
