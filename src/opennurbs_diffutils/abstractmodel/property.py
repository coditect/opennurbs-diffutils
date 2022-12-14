from typing import Type, Union

from .accessor import Accessor, PathAccessor
from .value import Value


class Property:
    """Represents a property of a component."""

    __slots__ = ("_name", "_type", "_accessor", "affectedBy", "deltaOnly")

    def __init__(
        self,
        name: str,
        type: Type[Value],
        accessor: Union[Accessor, str],
        affectedBy: "Property" = None,
        deltaOnly: bool = False,
    ):
        self._name = name
        self._type = type
        self._accessor = PathAccessor.ifString(accessor)
        self.affectedBy = affectedBy
        self.deltaOnly = deltaOnly

    @property
    def name(self) -> str:
        """The name of the property."""
        return self._name

    @property
    def type(self) -> Type[Value]:
        """The type of the property."""
        return self._type

    def getValue(self, component: "Component") -> Value:
        """Returns the value of the property for the given component."""
        return self._type(self._accessor.get(component))

    def setValue(self, component: "Component", value: Value):
        """Assigns the given value to the property on the given component."""
        self._accessor.set(component, value.value)

    def __hash__(self) -> int:
        return hash(self._name.casefold())

    def __eq__(self, other: "Property | str") -> bool:
        """Two properties are considered equal if they share the same name.
        Additionally, a string that consists of the property's name is also
        considered equal to the property. Names are compared on a
        case-insensitive basis."""
        if isinstance(other, Property):
            return self._name.casefold() == other.name.casefold()
        if isinstance(other, str):
            return self._name.casefold() == other.casefold()
        return False

    def __str__(self) -> str:
        return self._name
