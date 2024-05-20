
from typing import Dict
from gis.layers.layer.main import Layer

from .accessors import Accessors
from .handlers import Handlers
from ..distance_index_elements import IndexElement

class DistanceIndex(Accessors, Handlers):
    _distances: Dict[int, IndexElement]
    _road_layer: Layer
    _point_layer: Layer

    def __init__(self,
        road_layer: Layer,
        points_layer: Layer,
        distance_index_path: str = None
    ):
        self._road_layer = road_layer
        self._point_layer = points_layer
        if distance_index_path:
            distance_index = self._load_from_file(distance_index_path)
            self._distances = self._build_distance_elements(distance_index)
        else:
            self._distances = self._build_distance_index_from_layers()
