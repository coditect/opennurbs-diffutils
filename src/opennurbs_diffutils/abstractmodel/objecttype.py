from collections import OrderedDict
from .property import Property


class BaseType:
    """Enumerates the properties belonging to a type of object."""

    __slots__ = "_properties"

    def __init__(self, properties: list[Property]):
        self._properties = OrderedDict([(p.name.casefold(), p) for p in properties])

    @property
    def properties(self):
        """The list of properties supported by objects of this type."""
        yield from self._properties.values()

    def getProperty(self, name: str) -> Property:
        """Returns the property with the given name.

        Property names are compared case-insensitively.
        """
        try:
            return self._properties[name.casefold()]
        except KeyError:
            raise ValueError("{self._name} has no property '{name}'")
