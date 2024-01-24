from qgis.core import (
    QgsFeature
)

class Line:
    __feature: QgsFeature = None

    def __init__(self, feature: QgsFeature):
        self.__feature = feature

    def geometry(self):
        return self.__feature.geometry()

    def project(self, point: QgsFeature):
        return self.geometry().closestSegmentWithContext(point.geometry().asPoint())[1]

    def id(self):
        return self.__feature['fid']
