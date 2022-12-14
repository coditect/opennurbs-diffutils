import rhino3dm

from ..abstractmodel import ComponentType, ComponentTypeRegistry

from . import tables
from . import properties as props


class DummyGeometricObject:
    # Mimics the api of rhino3dm.File3dmObject
    def __init__(self, geometry, attributes=rhino3dm.ObjectAttributes()):
        self.Geometry = geometry
        self.Attributes = attributes


class NormalComponentType(ComponentType):
    def create(self, model):
        object = super().create(model)
        return tables.File3dmComponentWrapper(object, model)


class GeometricObjectType(ComponentType):
    def create(self, model):
        geometry = super().create(model)
        dummy = DummyGeometricObject(geometry)
        return tables.File3dmComponentWrapper(dummy, model)


class File3dmComponentTypeRegistry(ComponentTypeRegistry):
    def fromInstance(self, obj) -> ComponentType:
        if isinstance(obj, rhino3dm.File3dmObject):
            obj = obj.Geometry
        return super().fromInstance(obj)


def createLineCurve(*args):
    return rhino3dm.LineCurve(rhino3dm.Point3d(0, 0, 0), rhino3dm.Point3d(0, 0, 0))


def createTextDot():
    return rhino3dm.TextDot("", rhino3dm.Point3d(0, 0, 0))


ENTITY_TYPES = File3dmComponentTypeRegistry(
    [
        NormalComponentType(
            "Layer", rhino3dm.Layer, tables.LAYER_TABLE, props.LayerProperties
        ),
        NormalComponentType(
            "Linetype",
            rhino3dm.Linetype,
            tables.LINETYPE_TABLE,
            props.LinetypeProperties,
        ),
        NormalComponentType(
            "Group", rhino3dm.Group, tables.GROUP_TABLE, props.GroupProperties
        ),
        GeometricObjectType(
            "Point", rhino3dm.Point, tables.GEOMETRY_TABLE, props.PointProperties
        ),
        GeometricObjectType(
            "LineCurve",
            rhino3dm.LineCurve,
            tables.GEOMETRY_TABLE,
            props.LineCurveProperties,
            createDefault=createLineCurve,
        ),
        GeometricObjectType(
            "ArcCurve",
            rhino3dm.ArcCurve,
            tables.GEOMETRY_TABLE,
            props.ArcCurveProperties,
        ),
        GeometricObjectType(
            "TextDot",
            rhino3dm.TextDot,
            tables.GEOMETRY_TABLE,
            props.TextDotProperties,
            createDefault=createTextDot,
        ),
        # GeometricObjectType("PolylineCurve", rhino3dm.PolylineCurve, tables.Geometry, properties.GeometryProperties + [
        #     Property("Point", codecs.Point3d, )
        # ]),
        ComponentType(
            "Material",
            rhino3dm.Material,
            tables.MATERIAL_TABLE,
            props.MATERIAL_PROPERTIES,
        ),
    ]
)
