from .componenttype import ComponentTypeRegistry
from .objecttype import BaseType
from .property import Property
from .table import Table


class ModelType(BaseType):
    """Describes a type of model."""

    def __init__(
        self,
        tables: list[Table],
        componentTypes: ComponentTypeRegistry,
        properties: list[Property],
    ):
        super().__init__(properties)
        self.tables = tables
        self.componentTypes = componentTypes
