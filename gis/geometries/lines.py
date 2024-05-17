from qgis.core import QgsFeature

class Line:
    __feature: QgsFeature = None

    def __init__(self, feature: QgsFeature):
        self.__feature = feature

    def geometry(self):
        return self.__feature.geometry()

    def feature(self):
        return self.__feature

    def project(self, point: QgsFeature):
        from gis import Point

        shortest_line_geometry = self.geometry().shortestLine(point.geometry())
        intersection_point = shortest_line_geometry.intersection(self.geometry())
        feature = QgsFeature()
        feature.setGeometry(intersection_point)
        feature.setAttributes(point.feature().attributes())
        return Point(feature)

    def id(self):
        return self.__feature['fid']

    def length(self):
        return self.geometry().length()
    
    def length_to(self, point):
        return self.geometry().lineLocatePoint(point.geometry())
