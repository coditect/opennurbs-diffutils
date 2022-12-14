from uuid import UUID
from rhino3dm import File3dm

from wrapt import ObjectProxy
from ..abstractmodel import Table


class File3dmComponentWrapper(ObjectProxy):
    def __init__(self, component, model):
        super().__init__(component)
        self._self_model = model

    @property
    def model(self):
        return self._self_model


class File3dmTable(Table):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def getTable(self, model: File3dm):
        return getattr(model, self.name)

    def getComponent(self, model, id):
        table = self.getTable(model)
        object = table.FindId(id)
        return File3dmComponentWrapper(object, model)

    def allComponents(self, model):
        table = self.getTable(model)
        for component in table:
            yield File3dmComponentWrapper(component, model)

    @staticmethod
    def getComponentId(component):
        return component.Id

    @staticmethod
    def setComponentId(component, id):
        component.Id = id

    def idFromIndex(self, index: int, model: File3dm) -> UUID:
        table = self.getTable(model)
        return self.getComponentId(table[index])

    def indexFromId(self, id: UUID, model: File3dm) -> int:
        table = self.getTable(model)
        object = table.FindId(id)
        return object.Index

    def addComponent(self, component, model: File3dm):
        self.getTable(model).Add(component.__wrapped__)

    def deleteComponent(self, component, model: File3dm):
        self.getTable(model).Delete(component)


class GeometricObjectTable(File3dmTable):
    @staticmethod
    def getComponentId(component):
        return component.Attributes.Id

    @staticmethod
    def setComponentId(component, id):
        component.Attributes.Id = id

    def addComponent(self, component, model: File3dm):
        self.getTable(model).Add(component.Geometry, component.Attributes)

    def deleteComponent(self, component, model: File3dm):
        self.getTable(model).Delete(component)


BITMAP_TABLE = File3dmTable("Bitmaps")
DIMENSION_STYLE_TABLE = File3dmTable("DimStyles")
GEOMETRY_TABLE = GeometricObjectTable("Objects")
GROUP_TABLE = File3dmTable("Groups")
# HatchPatterns
# HistoryRecords
INSTANCE_DEFINITION_TABLE = File3dmTable("InstanceDefinitions")
LAYER_TABLE = File3dmTable("Layers")
LINETYPE_TABLE = File3dmTable("Linetypes")
MATERIAL_TABLE = File3dmTable("Materials")
NAMED_VIEW_TABLE = File3dmTable("NamedViews")
# PluginData
# TextStyles
# TextureMappings
VIEW_TABLE = File3dmTable("Views")


ALL_TABLES: list[Table] = [
    GEOMETRY_TABLE,
    GROUP_TABLE,
    LAYER_TABLE,
    LINETYPE_TABLE,
    MATERIAL_TABLE,
]
