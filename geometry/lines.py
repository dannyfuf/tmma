from qgis.core import *

def create_line(
    object: QgsFeature
):
    return object.geometry()
