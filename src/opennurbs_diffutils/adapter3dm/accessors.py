from typing import Union
from ..abstractmodel import Accessor, PathAccessor, Table, UUIDValue


class IndexReferenceAccessor:
    def __init__(self, baseAccessor: Union[Accessor, str], table: Table):
        self._baseAccessor = PathAccessor.ifString(baseAccessor)
        self._table = table

    def get(self, component):
        index = self._baseAccessor.get(component)
        return self._table.idFromIndex(index, component.model)

    def set(self, component, value: UUIDValue):
        index = self._table.indexFromId(value, component.model)
        self._baseAccessor.set(component, index)


class ValueObjectAccessor(Accessor):

    __slots__ = ("_objectAccessor", "_propertyAccessor")

    def __init__(
        self,
        objectAccessor: Union[Accessor, str],
        propertyAccessor: Union[Accessor, str],
    ):
        self._objectAccessor = PathAccessor.ifString(objectAccessor)
        self._propertyAccessor = PathAccessor.ifString(propertyAccessor)

    def get(self, host):
        return self._propertyAccessor.get(self._objectAccessor.get(host))

    def set(self, host, value):
        immutable_object = self._objectAccessor.get(host)
        self._propertyAccessor.set(immutable_object, value)
        self._objectAccessor.set(host, immutable_object)
