
from gis.layers.layer.main import Layer
from tmma.distance_index import DistanceIndex
from tmma.preprocesing.buffer_tuner import BufferTuner


class Preprocessing:
    buffer_size: float
    filtered_roads: Layer

    def __init__(
            self,
            road_layer: Layer,
            points_layer: Layer,
            distance_index: DistanceIndex
        ):
        self._road_layer = road_layer
        self._points_layer = points_layer
        self._distance_index = distance_index

    def run(self):
        buffer_tuner = BufferTuner(self._distance_index)
        buffer_size = buffer_tuner.get_buffer()
        self.buffer_size = buffer_size
        print(f'buffer size: {buffer_size}')

        self._distance_index.remove_roads_outside_buffer(buffer_size)
        self._distance_index.save_to('.data/.distance_index_filtered.json')
        norm_filtered_roads = self._distance_index.build_road_layer_from_distance_index()
        norm_filtered_roads.save_to(f'.data/{norm_filtered_roads.name()}_cleaned.gpkg')
        self.filtered_roads = norm_filtered_roads

