from qgis.core import QgsFeature

class Line:
    __feature: QgsFeature = None

    def __init__(self, feature: QgsFeature):
        self.__feature = feature

    def geometry(self):
        return self.__feature.geometry()

    def feature(self):
        return self.__feature

    def project(self, point):
        from gis import Point

        nearest_point = self.geometry().nearestPoint(point.geometry())
        feature = QgsFeature()
        feature.setGeometry(nearest_point)
        feature.setAttributes(point.feature().attributes())
        return Point(feature)

    def id(self):
        return self.__feature['fid']

    def length(self):
        return self.geometry().length()
    
    def length_to(self, point):
        return self.geometry().lineLocatePoint(point.geometry())

    def intersection(self, other):
        from gis import Point
        intersection = self.geometry().intersection(other.geometry())
        if intersection.isEmpty():
            return None
        else:
            feature = QgsFeature()
            feature.setGeometry(intersection)
            return Point(feature)