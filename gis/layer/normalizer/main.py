from qgis.core import (
    QgsVectorLayer,
    QgsCoordinateTransform,
    QgsProject,
    QgsCoordinateReferenceSystem,
)

from ..layer import Layer
from .accessors import Accessors
from .handlers import Handlers

class Normalizer(Accessors, Handlers):
    __default_crs: str = 'EPSG:32633'
    __crs_to: QgsCoordinateReferenceSystem = None
    __layer: Layer = None
    __transformer: QgsCoordinateTransform = None
    __normalized_layer: QgsVectorLayer = None

    def __init__(self, layer: Layer):
        self.__layer = layer
        self.__crs_to = QgsCoordinateReferenceSystem(self.default_crs())
        self.__transformer = self.build_crs_transformer(
            crs_from=self.layer().crs(),
            context=QgsProject.instance()
        )
