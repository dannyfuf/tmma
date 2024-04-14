from qgis.core import (
    QgsVectorLayer,
    QgsCoordinateTransform,
    QgsProject,
    QgsCoordinateReferenceSystem,
)

from ..layer.main import Layer
from .accessors import Accessors
from .handlers import Handlers

class Normalizer(Accessors, Handlers):
    _default_crs: str = 'EPSG:32633'
    _crs_to: QgsCoordinateReferenceSystem = None
    _layer: Layer = None
    _transformer: QgsCoordinateTransform = None
    _normalized_layer: QgsVectorLayer = None

    def __init__(self, layer: Layer):
        self._layer = layer
        self._crs_to = QgsCoordinateReferenceSystem(self.default_crs())
        self._transformer = self.build_crs_transformer(
            crs_from=self.layer().crs(),
            context=QgsProject.instance()
        )
