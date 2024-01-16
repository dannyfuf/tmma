from qgis.core import (
    QgsVectorLayer,
    QgsCoordinateTransform,
    QgsProject,
    QgsCoordinateReferenceSystem,
    QgsFields,
    QgsGeometry,
    QgsFeature,
)

from .types.normalizer import NormalizeCRSParams, LayerType
from .layers import Layer

class Normalizer:
    __default_crs: str = 'EPSG:32633'
    __crs_to: QgsCoordinateReferenceSystem = None
    __layer: Layer = None
    __transformer: QgsCoordinateTransform = None
    __normalized_layer: QgsVectorLayer = None

    def __init__(self, layer: Layer):
        self.__layer = layer
        self.__initialize_params()

    def __initialize_params(self):
        self.__crs_to = QgsCoordinateReferenceSystem(self.default_crs())
        self.__transformer = self.__create_crs_transformer({
            'crs_from': self.layer().crs(),
            'context': QgsProject.instance()
        })
    
    def __create_crs_transformer(self, params: NormalizeCRSParams):
        transformer = QgsCoordinateTransform(params['crs_from'], self.crs_to(), QgsProject.instance())
        return transformer

    def default_crs(self):
        return self.__default_crs

    def crs_to(self):
        return self.__crs_to

    def layer(self):
        return self.__layer

    def transformer(self):
        return self.__transformer
    
    def normalized_layer(self):
        return self.__normalized_layer

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
