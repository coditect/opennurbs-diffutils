import rhino3dm

from ..abstractmodel import EnumeratedValue


ActiveSpace = EnumeratedValue.defineSubclass(
    "ActiveSpace",
    "active space",
    {
        getattr(rhino3dm.ActiveSpace, "None"): "none",
        rhino3dm.ActiveSpace.ModelSpace: "model",
        rhino3dm.ActiveSpace.PageSpace: "page",
    },
)

# BlendContinuity = Lookup("blend continuity", {
#     rhino3dm.BlendContinuity.Curvature: "curvature",
#     rhino3dm.BlendContinuity.Position: "position",
#     rhino3dm.BlendContinuity.Tangency: "tangency",
# })

ColorSource = EnumeratedValue.defineSubclass(
    "ColorSource",
    "color source",
    {
        rhino3dm.ObjectColorSource.ColorFromLayer: "layer",
        rhino3dm.ObjectColorSource.ColorFromMaterial: "material",
        rhino3dm.ObjectColorSource.ColorFromObject: "object",
        rhino3dm.ObjectColorSource.ColorFromParent: "parent",
    },
)

Decoration = EnumeratedValue.defineSubclass(
    "Decoration",
    "object decoration",
    {
        getattr(rhino3dm.ObjectDecoration, "None"): "none",
        rhino3dm.ObjectDecoration.BothArrowhead: "both",
        rhino3dm.ObjectDecoration.StartArrowhead: "start",
        rhino3dm.ObjectDecoration.EndArrowhead: "end",
    },
)

UnitSystem = EnumeratedValue.defineSubclass(
    "UnitSystem",
    "unit system",
    {
        getattr(rhino3dm.ActiveSpace, "None"): "none",
        rhino3dm.UnitSystem.Angstroms: "angstroms",
        rhino3dm.UnitSystem.Nanometers: "nanometers",
        rhino3dm.UnitSystem.Microns: "microns",
        rhino3dm.UnitSystem.Millimeters: "millimeters",
        rhino3dm.UnitSystem.Centimeters: "centimeters",
        rhino3dm.UnitSystem.Decimeters: "decimeters",
        rhino3dm.UnitSystem.Meters: "meters",
        rhino3dm.UnitSystem.Dekameters: "dekameters",
        rhino3dm.UnitSystem.Hectometers: "hectometers",  # spelling
        rhino3dm.UnitSystem.Kilometers: "kilometers",
        rhino3dm.UnitSystem.Megameters: "megameters",
        rhino3dm.UnitSystem.Gigameters: "gigameters",
        rhino3dm.UnitSystem.Microinches: "microinches",
        rhino3dm.UnitSystem.Mils: "mils",
        rhino3dm.UnitSystem.Inches: "inches",
        rhino3dm.UnitSystem.Feet: "feet",
        rhino3dm.UnitSystem.Yards: "yards",
        rhino3dm.UnitSystem.Miles: "miles",
        rhino3dm.UnitSystem.PrinterPoints: "points",
        rhino3dm.UnitSystem.PrinterPicas: "picas",
        rhino3dm.UnitSystem.NauticalMiles: "nautical-miles",
        rhino3dm.UnitSystem.AstronomicalUnits: "astronomical-units",
        rhino3dm.UnitSystem.LightYears: "light-years",
        rhino3dm.UnitSystem.Parsecs: "parsecs",
        rhino3dm.UnitSystem.CustomUnits: "custom",
        rhino3dm.UnitSystem.Unset: "unset",
    },
)

LinetypeSource = EnumeratedValue.defineSubclass(
    "LinetypeSource",
    "linetype source",
    {
        rhino3dm.ObjectLinetypeSource.LinetypeFromLayer: "layer",
        rhino3dm.ObjectLinetypeSource.LinetypeFromObject: "object",
        rhino3dm.ObjectLinetypeSource.LinetypeFromParent: "parent",
    },
)

# LoftType = EnumeratedValue.defineSubclass("LoftType", "loft type", {
#     rhino3dm.LoftType.Loose: "loose",
#     rhino3dm.LoftType.Normal: "normal",
#     rhino3dm.LoftType.Straight: "straight",
#     rhino3dm.LoftType.Tight: "tight",
#     rhino3dm.LoftType.Uniform: "uniform",
# })

MaterialSource = EnumeratedValue.defineSubclass(
    "MaterialSource",
    "material source",
    {
        rhino3dm.ObjectMaterialSource.MaterialFromLayer: "layer",
        rhino3dm.ObjectMaterialSource.MaterialFromObject: "object",
        rhino3dm.ObjectMaterialSource.MaterialFromParent: "parent",
    },
)

ObjectMode = EnumeratedValue.defineSubclass(
    "ObjectMode",
    "object mode",
    {
        rhino3dm.ObjectMode.Hidden: "hidden",
        rhino3dm.ObjectMode.InstanceDefinitionObject: "instanceDefinition",
        rhino3dm.ObjectMode.Locked: "locked",
        rhino3dm.ObjectMode.Normal: "normal",
    },
)

PlotColorSource = EnumeratedValue.defineSubclass(
    "PlotColorSource",
    "plot color source",
    {
        rhino3dm.ObjectPlotColorSource.PlotColorFromDisplay: "display",
        rhino3dm.ObjectPlotColorSource.PlotColorFromLayer: "layer",
        rhino3dm.ObjectPlotColorSource.PlotColorFromObject: "object",
        rhino3dm.ObjectPlotColorSource.PlotColorFromParent: "parent",
    },
)

PlotWeightSource = EnumeratedValue.defineSubclass(
    "PlotWeightSource",
    "plot weight source",
    {
        rhino3dm.ObjectPlotWeightSource.PlotWeightFromLayer: "layer",
        rhino3dm.ObjectPlotWeightSource.PlotWeightFromObject: "object",
        rhino3dm.ObjectPlotWeightSource.PlotWeightFromParent: "parent",
    },
)

ShadowMapLevel = EnumeratedValue.defineSubclass(
    "ShadowMapLevel",
    "shadow map level",
    {
        0: "none",
        1: "normal",
        2: "best",
    },
)

InstanceDefinitionUpdateType = EnumeratedValue.defineSubclass(
    "InstanceDefinitionUpdateType",
    "instance definition type",
    {
        rhino3dm.InstanceDefinitionUpdateType.Embedded: "embedded",
        rhino3dm.InstanceDefinitionUpdateType.Linked: "linked",
        rhino3dm.InstanceDefinitionUpdateType.LinkedAndEmbedded: "linkedAndEmbedded",
        rhino3dm.InstanceDefinitionUpdateType.Static: "static",
    },
)
