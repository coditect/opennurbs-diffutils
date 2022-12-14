from abc import ABC, abstractmethod
import re
from typing import TextIO
from uuid import UUID

from .commontypes import Model
from .componenttype import ComponentType, ComponentTypeRegistry
from .propertymap import PropertyDeltaMap, PropertyValueMap
from .session import Session


class ComponentDelta(ABC):
    """Describes the changes to a single model component."""

    SYMBOL: str
    _CLASSES_BY_SYMBOL = {}
    _HEADER_PATTERN = re.compile(r"^@@\s+([-+~])(\w+)\s+([-0-9a-f]+)")

    def __init__(self, type: ComponentType, id: UUID):
        self.type = type
        """The type of the component."""
        self.id = id
        """The ID of the component."""

    def __init_subclass__(cls, symbol, **kwargs):
        cls._SYMBOL = symbol
        ComponentDelta._CLASSES_BY_SYMBOL[symbol] = cls

    def write(self, output: TextIO):
        """Writes a textual representation of the object to the given output stream."""
        output.write(f"@@ {self._SYMBOL}{self.type.name} {self.id} @@\n")
        self.properties.write(output)

    def readline(self, line: str):
        """Parses a property and value or delta from the given string and adds them to the object's property map."""
        self.properties.readline(line, self.type)

    @abstractmethod
    def apply(self, model: Model, session: Session):
        """Applies the changes described in this object to the given model."""

    @abstractmethod
    def reverse(self):
        """Returns a ComponentDelta that has the opposite meaning of this one."""

    def merge(self, other: "ComponentDelta", session: Session):
        """Returns a ComponentDelta that inclues both the changes listed in this object as well those listed in another."""
        if self.__class__ != other.__class__:
            raise Exception(
                f"Cannot merge components with id {self.id}: Incompatible operations"
            )
        if self.type != other.type:
            raise Exception(
                f"Cannot merge components with id {self.id}: Incompatible component types"
            )
        merged = self.__class__(self.type, self.id)
        merged.properties = self.properties.merge(other.properties)
        return merged

    @staticmethod
    def fromHeader(header: str, componentTypes: ComponentTypeRegistry):
        """Creates an empty ComponentDelta from a header line."""
        match = ComponentDelta._HEADER_PATTERN.match(header)
        if not match:
            raise ValueError("Malformed header")
        cls = ComponentDelta._CLASSES_BY_SYMBOL[match[1]]
        type = componentTypes.findByName(match[2])  # throws if not found
        uuid = UUID(match[3])  # throws if invalid format
        return cls(type, uuid)


class ComponentAddition(ComponentDelta, symbol="+"):
    """Represents the addition of a component to a model."""

    def __init__(self, type: ComponentType, id: UUID):
        super().__init__(type, id)
        self.properties = PropertyValueMap()
        """The non-default properties of the object that was added."""

    def apply(self, model, session: Session):
        component = self.type.create(model)
        self.type._table.setComponentId(component, self.id)
        self.properties.apply(component, session)
        self.type._table.addComponent(component, model)

    def reverse(self):
        reversed = ComponentDeletion(self.type, self.id)
        reversed.properties = self.properties[:]
        return reversed


class ComponentDeletion(ComponentDelta, symbol="-"):
    """Represents the deletion of a component from a model."""

    def __init__(self, type: ComponentType, id: UUID):
        super().__init__(type, id)
        self.properties = PropertyValueMap()
        """The non-default properties of the object that was deleted."""

    def apply(self, model: Model, session: Session):
        self.type._table.deleteComponent(self.id, model)

    def reverse(self):
        reversed = ComponentAddition(self.type, self.id)
        reversed.properties = self.properties[:]
        return reversed


class ComponentModification(ComponentDelta, symbol="~"):
    """Describes the changes to a component that exists in two versions of a model."""

    def __init__(self, type: ComponentType, id: UUID):
        super().__init__(type, id)
        self.properties = PropertyDeltaMap()
        """The properties of the object that have been modified."""

    def write(self, output: TextIO):
        if len(self.properties) > 0:
            super().write(output)

    def apply(self, model: Model, session: Session):
        component = self.type._table.getComponent(
            model, self.id
        )
        self.properties.apply(component, session)

    def reverse(self):
        reversed = ComponentModification(self.type, self.id)
        reversed.properties = self.properties.reverse()
        return reversed
