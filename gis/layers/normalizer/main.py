from qgis.core import (
    QgsVectorLayer,
    QgsCoordinateTransform,
    QgsCoordinateReferenceSystem,
)

from ..layer.main import Layer
from .accessors import Accessors
from .handlers import Handlers

class Normalizer(Accessors, Handlers):
    _default_crs: str = 'EPSG:32633'
    _crs_to: QgsCoordinateReferenceSystem = None
    _transformer: QgsCoordinateTransform = None
    _normalized_layer: QgsVectorLayer = None

    def __init__(self):
        self._crs_to = QgsCoordinateReferenceSystem(self.default_crs())
