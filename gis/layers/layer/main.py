from qgis.core import QgsVectorLayer
from .accessors import Accessors
from .handlers import Handlers

class Layer(Accessors, Handlers):
    _layer: QgsVectorLayer = None

    def __init__(self, layer: QgsVectorLayer = None):
        self._layer = layer

    def new(self, layer_type: str, layer_name: str, layer_crs: str):
        self._layer = QgsVectorLayer(f"{layer_type}?crs={layer_crs}", layer_name, "memory")
        return self
