from typing import Union
from qgis.core import QgsFeature
from datetime import datetime

from .lines import Line

class Point:
    __feature: QgsFeature = None

    def __init__(self, feature: QgsFeature):
        self.__feature = feature

    def geometry(self):
        return self.__feature.geometry()

    def distance_to(self, target: Union['Point', Line]):
        if type(target) == Point:
            point_geometry = target.geometry()
        elif type(target) == Line:
            point_geometry = target.project(self.__feature)

        return self.geometry().asPoint().distance(point_geometry)
    
    def time_to(self, point: QgsFeature, field_name='Time'):
        format = "%I:%M:%S %p"
        time_i = datetime.strptime(self.__feature[field_name], format)
        time_j = datetime.strptime(point[field_name], format)
        return (time_j - time_i).total_seconds()

    def speed(self, field_name='Speed'):
        return self.__feature[field_name]
    
    def buffer(self, radius: float, segments=10):
        return self.__geometry.buffer(radius, segments)

    def id(self):
        return self.__feature['fid']