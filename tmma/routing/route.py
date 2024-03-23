from ..distance_index.main import DistanceIndex

class Route:
    __distance_index: DistanceIndex

    def __init__(self, distance_index):
        self.__distance_index = distance_index

    
