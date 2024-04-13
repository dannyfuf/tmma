from qgis.core import QgsWkbTypes

class Accessors:
    def layer(self):
        return self._layer

    def name(self):
        return self.layer().name()

    def crs(self):
        return self.layer().crs()
    
    def crs_name(self):
        return self.layer().crs().authid()

    def units(self):
        return self.layer().crs().mapUnits()
    
    def fields(self):
        return self.layer().fields()
    
    def field_names(self):
        return list(map(lambda field: field.name(), self.fields()))
    
    def features(self):
        return self.layer().getFeatures()
    
    def add_feature(self, feature):
        self.layer().addFeature(feature)

    def type(self):
        layer_type = self.layer().wkbType()
        if layer_type == QgsWkbTypes.MultiLineString:
            return 'MultiLineString'
        elif layer_type == QgsWkbTypes.Point:
            return 'MultiPoint'
        elif layer_type == QgsWkbTypes.MultiPoint:
            return 'MultiPoint'
        else:
            raise Exception('Layer type not supported')