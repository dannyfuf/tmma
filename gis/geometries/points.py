from qgis.core import QgsFeature
from datetime import datetime

class Point:
    __feature: QgsFeature = None

    def __init__(self, feature: QgsFeature):
        self.__feature = feature
        self.__geometry = self.__get_geometry(feature)

    def distance_to(self, point: QgsFeature):
        point_geometry = self.__get_geometry(point)
        return self.__geometry.distance(point_geometry)
    
    def time_to(self, point: QgsFeature, field_name='Time'):
        format = "%I:%M:%S %p"
        time_i = datetime.strptime(self.__feature[field_name], format)
        time_j = datetime.strptime(point[field_name], format)
        return (time_j - time_i).total_seconds()

    def speed(self, field_name='Speed'):
        return self.__feature[field_name]
    
    def buffer(self, radius: float, segments=10):
        return self.__geometry.buffer(radius, segments)
    
    def __get_geometry(self, feature: QgsFeature):
        return feature.geometry()


# ------------------------------------------------------------
#                         BUILDERS
# ------------------------------------------------------------

def create_point(
    object: QgsFeature,
    x_name='X',
    y_name='Y'
):
    x, y = object[x_name], object[y_name]
    point_xy = QgsPointXY(x, y)
    return QgsGeometry.fromPointXY(point_xy)

def create_buffer(
    point: QgsGeometry,
    radius: float,
    segments=10
):
    return point.buffer(radius, segments)


def point_to_feature(
    point: QgsPointXY,
    fields: QgsFields
):
    feature = QgsFeature(fields)
    feature.setGeometry(point)
    return feature

# ------------------------------------------------------------
#                         GETTERS
# ------------------------------------------------------------

# def get_distance_between_points(
#     point_i: QgsGeometry,
#     point_j: QgsGeometry
# ):
#     return point_i.distance(point_j)

# def get_time_between_points(
#     point_i: QgsFeature,
#     point_j: QgsFeature,
#     field_name='Time'
# ):
#     format = "%I:%M:%S %p"
#     time_i = datetime.strptime(point_i[field_name], format)
#     time_j = datetime.strptime(point_j[field_name], format)
#     return (time_j - time_i).total_seconds()

# def get_point_speed(point: QgsFeature, field_name='Speed'):
#     return point[field_name]


def get_first_point(layer: QgsVectorLayer):
    expresion_orden = QgsFeatureRequest.OrderBy([QgsFeatureRequest.OrderByClause('Time', ascending=True)])
    request = QgsFeatureRequest().setOrderBy(expresion_orden).setLimit(1)
    features = list(layer.getFeatures(request))
    return str(features[0]['fid'])

def get_points_order(layer: QgsVectorLayer):
    sort_expression = QgsFeatureRequest.OrderBy([QgsFeatureRequest.OrderByClause('timestamp', ascending=True)])
    request = QgsFeatureRequest().setOrderBy(sort_expression)
    feature_iterator = layer.getFeatures(request)
    id_list = []

    for feature in feature_iterator:
        id_list.append(feature['fid'])
    
    return id_list
