from ..abstractmodel import (
    Property,
    BooleanValue,
    FloatValue,
    IntegerValue,
    StringValue,
    UUIDValue,
)
from .accessors import IndexReferenceAccessor, ValueObjectAccessor

from . import enums
from . import tables
from . import value_types


ModelProperties = [
    Property("BasePoint", value_types.Point3d, "Settings.ModelBasePoint"),
    Property("URL", StringValue, "Settings.ModelUrl"),
    # EarthAnchorPoint
    # CurrentColor, CurrentColorSource, etc.
    Property("ModelAbsoluteTolerance", FloatValue, "Settings.ModelAbsoluteTolerance"),
    Property("ModelAngleTolerance", FloatValue, "Settings.ModelAngleToleranceRadians"),
    Property("ModelRelativeTolerance", FloatValue, "Settings.ModelRelativeTolerance"),
    Property("ModelUnitSystem", enums.UnitSystem, "Settings.ModelUnitSystem"),
    Property("PageAbsoluteTolerance", FloatValue, "Settings.PageAbsoluteTolerance"),
    Property("PageAngleTolerance", FloatValue, "Settings.PageAngleToleranceRadians"),
    Property("PageRelativeTolerance", FloatValue, "Settings.PageRelativeTolerance"),
    Property("PageUnitSystem", enums.UnitSystem, "Settings.PageUnitSystem"),
    Property("AmbientLight", value_types.Color, "Settings.RenderSettings.AmbientLight"),
    Property(
        "BackgroundColorTop",
        value_types.Color,
        "Settings.RenderSettings.BackgroundColorTop",
    ),
    Property(
        "BackgroundColorBottom",
        value_types.Color,
        "Settings.RenderSettings.BackgroundColorBottom",
    ),
    Property(
        "UseHiddenLights", BooleanValue, "Settings.RenderSettings.UseHiddenLights"
    ),
    Property("DepthCue", BooleanValue, "Settings.RenderSettings.DepthCue"),
    Property("FlatShade", BooleanValue, "Settings.RenderSettings.FlatShade"),
    Property(
        "RenderBackFaces", BooleanValue, "Settings.RenderSettings.RenderBackFaces"
    ),
    Property("RenderPoints", BooleanValue, "Settings.RenderSettings.RenderPoints"),
    Property("RenderCurves", BooleanValue, "Settings.RenderSettings.RenderCurves"),
    Property(
        "RenderIsoParams", BooleanValue, "Settings.RenderSettings.RenderIsoParams"
    ),
    Property(
        "RenderMeshEdges", BooleanValue, "Settings.RenderSettings.RenderMeshEdges"
    ),
    Property(
        "RenderAnnotations", BooleanValue, "Settings.RenderSettings.RenderAnnotations"
    ),
    Property(
        "UseViewportSize", BooleanValue, "Settings.RenderSettings.UseViewportSize"
    ),
    Property(
        "ScaleBackgroundToFit",
        BooleanValue,
        "Settings.RenderSettings.ScaleBackgroundToFit",
    ),
    Property(
        "TransparentBackground",
        BooleanValue,
        "Settings.RenderSettings.TransparentBackground",
    ),
    Property("ImageDpi", FloatValue, "Settings.RenderSettings.ImageDpi"),
    Property(
        "ShadowMapLevel", enums.ShadowMapLevel, "Settings.RenderSettings.ShadowMapLevel"
    ),
    # NamedView, SnapShot, SpecificViewport
]


CommonProperties = [
    Property("Name", StringValue, "Name"),
]


GeometryProperties = [
    Property("Color", value_types.Color, "Attributes.ObjectColor"),
    Property("ColorSource", enums.ColorSource, "Attributes.ColorSource"),
    Property("Decoration", enums.Decoration, "Attributes.ObjectDecoration"),
    Property("DisplayOrder", IntegerValue, "Attributes.DisplayOrder"),
    Property(
        "Layer",
        UUIDValue,
        IndexReferenceAccessor("Attributes.LayerIndex", tables.LAYER_TABLE),
    ),
    Property(
        "Linetype",
        UUIDValue,
        IndexReferenceAccessor("Attributes.LinetypeIndex", tables.LINETYPE_TABLE),
    ),
    Property("LinetypeSource", enums.LinetypeSource, "Attributes.LinetypeSource"),
    Property(
        "Material",
        UUIDValue,
        IndexReferenceAccessor("Attributes.MaterialIndex", tables.MATERIAL_TABLE),
    ),
    Property("MaterialSource", enums.MaterialSource, "Attributes.MaterialSource"),
    Property("Name", StringValue, "Attributes.Name"),
    Property("PlotColor", value_types.Color, "Attributes.PlotColor"),
    Property("PlotColorSource", enums.PlotColorSource, "Attributes.PlotColorSource"),
    Property("PlotWeight", FloatValue, "Attributes.PlotWeight"),
    Property("PlotWeightSource", enums.PlotWeightSource, "Attributes.PlotWeightSource"),
    Property("Space", enums.ActiveSpace, "Attributes.ActiveSpace"),
    Property("Viewport", UUIDValue, "Attributes.ViewportId"),
    Property("WireDensity", IntegerValue, "Attributes.WireDensity"),
    Property("CastsShadows", BooleanValue, "Attributes.CastsShadows"),
    Property("ReceivesShadows", BooleanValue, "Attributes.ReceivesShadows"),
    Property("Mode", enums.ObjectMode, "Attributes.Mode"),
    Property("URL", StringValue, "Attributes.Url"),
    # Groups
    # Property("Groups", UUID_SET, FunctionalAccessor(getGroups, setGroups), tables.GROUP_TABLE),
    # IsInstanceDefinitionGeometry -- included in Mode?
]

PointProperties = GeometryProperties + [
    Property("Point", value_types.Point3d, "Geometry.Location"),
]

CurveProperties = GeometryProperties + [
    Property("Dimension", IntegerValue, "Geometry.Dimension"),
    Property("Domain", value_types.Interval, "Geometry.Domain"),
]

LineCurveGeometryProperty = Property(
    "Geometry", value_types.Line, "Geometry.Line", deltaOnly=True
)
LineCurveProperties = CurveProperties + [
    LineCurveGeometryProperty,
    Property(
        "StartPoint",
        value_types.Point3d,
        ValueObjectAccessor("Geometry.Line", "From"),
        affectedBy=LineCurveGeometryProperty,
    ),
    Property(
        "EndPoint",
        value_types.Point3d,
        ValueObjectAccessor("Geometry.Line", "To"),
        affectedBy=LineCurveGeometryProperty,
    ),
]


# Setting the center, normal, radius, or angle of an ArcCurve will require creating a whole new component!
ArcCuveGeometryProperty = Property(
    "Geometry", value_types.Arc, "Geometry.Arc", deltaOnly=True
)
ArcCurveProperties = CurveProperties + [
    Property(
        "Center",
        value_types.Point3d,
        ValueObjectAccessor("Geometry.Arc", "Center"),
        affectedBy=ArcCuveGeometryProperty,
    ),
    Property(
        "Normal",
        value_types.Vector3d,
        ValueObjectAccessor("Geometry.Arc", "Plane.ZAxis"),
        affectedBy=ArcCuveGeometryProperty,
    ),
    Property(
        "Radius",
        FloatValue,
        ValueObjectAccessor("Geometry.Arc", "Radius"),
        affectedBy=ArcCuveGeometryProperty,
    ),
    Property(
        "Angle",
        value_types.Interval,
        ValueObjectAccessor("Geometry.Arc", "AngleRadians"),
        affectedBy=ArcCuveGeometryProperty,
    ),
]


class PolylineCurvePointsAccessor:
    def getIndices(self, component):
        return (i for i in range(component.PointCount))

    def get(self, component, index):
        return component.Point(index)

    def set(self, component, index, value):
        component.SetPoint(index, value)


PolylineCurveProperties = CurveProperties = [
    Property("Points", value_types.Point3d, PolylineCurvePointsAccessor())
]

TextDotProperties = GeometryProperties + [
    Property("Point", value_types.Point3d, "Geometry.Point"),
    Property("PrimaryText", StringValue, "Geometry.Text"),
    Property("SecondaryText", StringValue, "Geometry.SecondaryText"),
    Property("FontFace", StringValue, "Geometry.FontFace"),
    Property("Height", IntegerValue, "Geometry.FontHeight"),
    # AlwaysOnTop, Bold, Italic, Transparent
]

LayerProperties = CommonProperties + [
    Property("Color", value_types.Color, "Color"),
    Property("IgesLevel", IntegerValue, "IgesLevel"),
    Property(
        "Linetype",
        UUIDValue,
        IndexReferenceAccessor("LinetypeIndex", tables.LINETYPE_TABLE),
    ),
    # Property("Index", IntegerValue, "Index"),
    Property(
        "Material",
        UUIDValue,
        IndexReferenceAccessor("RenderMaterialIndex", tables.MATERIAL_TABLE),
    ),
    Property("Parent", UUIDValue, "ParentLayerId"),
    Property("PlotColor", value_types.Color, "PlotColor"),
    Property("PlotWeight", FloatValue, "PlotWeight"),
]

GroupProperties = CommonProperties + []

# HatchPatternProperties = CommonProperties + [
#     Property("Description", ...)
# ]


def getSegments(linetype):
    return [linetype.GetSegment(i) for i in range(linetype.SegmentCount)]


def setSegments(linetype, segments):
    linetype.ClearPattern()
    for length, solid in segments:
        linetype.AppendSegment(length, solid)


LinetypeProperties = CommonProperties + [
    # Property("Segments", value_types.LINETYPE_SEGMENTS, FunctionalAccessor(getSegments, setSegments))
]


MATERIAL_PROPERTIES = CommonProperties + [
    Property("AmbientColor", value_types.Color, "AmbientColor"),
    Property("DiffuseColor", value_types.Color, "DiffuseColor"),
    Property("DisableLighting", BooleanValue, "DisableLighting"),
    Property("EmissionColor", value_types.Color, "EmissionColor"),
    Property("FresnelIndexOfRefraction", FloatValue, "FresnelIndexOfRefraction"),
    Property("FresnelReflections", BooleanValue, "FresnelReflections"),
    Property("IndexOfRefraction", FloatValue, "IndexOfRefraction"),
    Property("PreviewColor", value_types.Color, "PreviewColor"),
    Property("ReflectionColor", value_types.Color, "ReflectionColor"),
    Property("ReflectionGlossiness", FloatValue, "ReflectionGlossiness"),
    Property("Reflectivity", FloatValue, "Reflectivity"),
    Property("RenderPlugIn", UUIDValue, "RenderPlugInId"),
    Property("Shine", FloatValue, "Shine"),
    Property("SpecularColor", value_types.Color, "SpecularColor"),
    Property("Transparency", FloatValue, "Transparency"),
    Property("TransparentColor", value_types.Color, "TransparentColor"),
    # MaterialChannel
    # PhysicallyBased
    # RdkMaterialInstanceId
    # Textures
    # Shareable
    # UseDiffuseTextureAlphaForObjectTransparencyTexture
]

INSTANCE_DEFINITION_PROPERTIES = CommonProperties + [
    Property("Description", StringValue, "Description"),
    Property("SourceArchive", StringValue, "SourceArchive"),
    Property("Type", enums.InstanceDefinitionUpdateType, "UpdateType"),
    # URL
    # URL Tag
    # Others?
]
