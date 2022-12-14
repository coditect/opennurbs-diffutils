from abc import ABC, abstractmethod
from typing import TextIO, Type

from .commontypes import Pair
from .componenttype import ComponentType
from .property import Property
from .stringable import Stringable
from .session import Session


INDENT = "\t"


class PropertyMap(dict, ABC):
    """Correlates a Property to a Value or Delta."""

    def write(self, output: TextIO):
        """Writes a textual representation of the map to the given output stream."""
        for property, item in self.items():
            output.write(f"{INDENT}{property}: {item}\n")

    def readline(self, string: str, objectType: "ComponentType"):
        """Parses a property and value or delta from the given string and adds them to the map."""
        parts = string.split(":", 2)
        if len(parts) != 2:
            raise ValueError("Invalid line format")

        name = parts[0].strip()
        property = objectType.getProperty(name)  # throws if not found
        value, _ = self._stringableFromProperty(property).fromString(parts[1].strip())
        self[property] = value

    @abstractmethod
    def _stringableFromProperty(self, property: Property) -> Type[Stringable]:
        """Returns an class on which fromString() can be called to parse a value or delta."""

    @abstractmethod
    def apply(self, component: "Component", session: Session) -> None:
        """Applies the values or deltas listed in the map to the given component."""

    @abstractmethod
    def reverse(self) -> "PropertyMap":
        """Returns a PropertyMap that has the opposite meaning of this one."""

    @abstractmethod
    def merge(self, other: "PropertyMap") -> "PropertyMap":
        """Returns a PropertyMap that combines the properties listed in this map with those listed in another."""


class PropertyValueMap(PropertyMap):
    """Correlates a Property to a Value."""

    def _stringableFromProperty(self, property: Property):
        return property.type

    def apply(self, component, session: Session):
        """Assigns the values listed in this map to their corresponding properties on the given component."""
        for property, value in self.items():
            property.setValue(component, value)

    def reverse(self):
        return self

    def merge(self, other):
        merged = PropertyValueMap()
        for property, value in self.items():
            if property in other and value != other[property]:
                raise Exception(
                    f"Incompatible values for property {property} ({value} != {other[property]})"
                )
            merged[property] = value
        for property, value in other.items():
            if property not in self:
                merged[property] = value
        return merged

    @classmethod
    def fromNonDefaultValues(
        cls, properties: list[Property], component: "Component", default: "Component"
    ):
        """Creates a PropertyValueMap that discribes how the given component differs from the default state of a component of its type."""
        values = cls()
        for property in properties:
            if not property.deltaOnly:
                instanceValue = property.getValue(component)
                defaultValue = property.getValue(default)
                if instanceValue != defaultValue:
                    values[property] = instanceValue
        return values


class PropertyDeltaMap(PropertyMap):
    """Correlates a Property to a Delta."""

    def _stringableFromProperty(self, property: Property):
        return property.type.deltaType()

    def apply(self, component, session: Session):
        """Applies the deltas listed in this map to their corresponding properties on the given component."""
        for property, delta in self.items():
            currentValue = property.getValue(component)
            newValue = delta.apply(currentValue, session)
            property.setValue(component, newValue)

    def reverse(self):
        return PropertyDeltaMap(
            {property: delta.reverse() for property, delta in self.items()}
        )

    def merge(self, other):
        merged = PropertyDeltaMap()
        for property, value in self.items():
            if property in other and value != other[property]:
                raise Exception(
                    f"Incompatible values for property {property} ({value} != {other[property]})"
                )
            merged[property] = value
        for property, value in other.items():
            if property not in self:
                merged[property] = value
        return merged

    @classmethod
    def fromDifferences(
        cls, components: Pair["Component"], properties: list[Property], session: Session
    ):
        """Creates a PropertyDeltaMap that lists the differences between the given pair of components."""
        differences = PropertyDeltaMap()
        propertiesToCheck = list(properties)
        propertiesChecked = set()

        while len(propertiesToCheck) > 0:
            deferredProperties = []
            for property in propertiesToCheck:
                if property.affectedBy is None:
                    # print(f"{property} does not depend on any other properties")
                    olderValue = property.getValue(components[0])
                    newerValue = property.getValue(components[1])
                    if olderValue != newerValue:
                        differences[property] = olderValue.diff(newerValue)
                    propertiesChecked.add(property)
                elif property.affectedBy in propertiesChecked:
                    # print(f"{property} depends on {property.affectedBy}")
                    olderValue = property.getValue(components[0])
                    newerValue = property.getValue(components[1])
                    if property.affectedBy in differences:
                        olderValue = differences[property.affectedBy].apply(
                            olderValue, session
                        )
                    if olderValue != newerValue:
                        differences[property] = olderValue.diff(newerValue)
                    propertiesChecked.add(property)
                else:
                    # print("deferring", property)
                    deferredProperties.append(property)

            propertiesToCheck = deferredProperties

        return differences
