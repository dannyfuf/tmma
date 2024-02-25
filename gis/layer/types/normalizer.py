from typing import TypedDict, Literal
from qgis.core import QgsVectorLayer, QgsProject, QgsCoordinateReferenceSystem

class NormalizeCRSParams(TypedDict):
    crs_from: QgsCoordinateReferenceSystem
    context: QgsProject

LayerType = Literal['MultiLineString', 'MultiPoint']