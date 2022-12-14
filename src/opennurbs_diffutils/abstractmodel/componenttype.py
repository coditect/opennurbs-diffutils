# from collections import OrderedDict
from typing import Any, Callable, Generic, Type, TypeVar

from .objecttype import BaseType
from .property import Property
from .table import Table

T = TypeVar("T")


class ComponentType(BaseType, Generic[T]):
    """Describes a type of component."""

    __slots__ = ("_name", "_class", "_table", "_createDefault")

    def __init__(
        self,
        name: str,
        cls: Type[T],
        table: Table,
        properties: list[Property],
        createDefault: Callable[[Type[T], Any], T] = None,
    ):
        super().__init__(properties)
        self._name = name
        self._class = cls
        self._table = table
        self._createDefault = createDefault

    @property
    def name(self):
        """The name of the type."""
        return self._name

    def create(self, model):
        """Creates a new component of this type."""
        if self._createDefault:
            return self._createDefault(self._class, model)
        return self._class()


class ComponentTypeRegistry:
    """A collection of component types supported by a model format."""

    def __init__(self, types):
        self._typesByName = {}
        self._typesByClass = {}
        for type in types:
            self._typesByName[type._name.casefold()] = type
            self._typesByClass[type._class] = type

    def findByName(self, name: str) -> ComponentType:
        """Returns the component type with the given name.

        Component type names are compared case-insensitively."""
        try:
            return self._typesByName[name.casefold()]
        except KeyError:
            raise KeyError(f"Unrecongized component type '{name}'")

    def findByClass(self, cls: Type) -> ComponentType:
        """Returns the component type that corresponds to the given class."""
        try:
            return self._typesByClass[cls]
        except KeyError:
            raise KeyError(f"Unsupported component type '{cls.__qualname__}'")

    def fromInstance(self, obj: Any) -> ComponentType:
        """Returns the component type that corresponds to the class of the given object."""
        return self.findByClass(obj.__class__)
