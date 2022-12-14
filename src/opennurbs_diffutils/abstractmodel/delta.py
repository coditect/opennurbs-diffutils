from abc import abstractmethod
from functools import cache
import re
from typing import Generic, Type, TypeVar

from .session import Session
from .stringable import Stringable


T = TypeVar("T")


class Delta(Stringable, Generic[T]):
    """Describes how one value is changed into another."""

    @abstractmethod
    def __init__(self, olderValue: T, newerValue: T):
        pass

    @abstractmethod
    def apply(self, currentValue: T, session: Session) -> T:
        """Produces a new value by executing the change described by this object with the given value."""

    @abstractmethod
    def reverse(self) -> "Delta[T]":
        """Returns a Delta that performs the opposite change from this one."""

    @abstractmethod
    def __eq__(self, other) -> bool:
        """Compares this delta to another and returns true if they are equal."""


class Substitution(Delta[T]):
    """An implementation of Delta that simply replaces one value with another."""

    __slots__ = ("_older", "_newer")

    _DELIMITER = "->"
    _VALUE_TYPE: Type[T]

    def __init__(self, olderValue, newerValue):
        self._older = olderValue
        self._newer = newerValue

    def apply(self, currentValue, session: Session):
        if currentValue != self._older:
            session.warn(f"Expected a value of {self._older} but got {currentValue}")
            # session.warn(f"Value of {property.name} property is {property.format(current)}; expected {property.format(value[0])}")
        return self._newer

    def reverse(self):
        return Substitution(self._newer, self._older)

    def __str__(self):
        return f"{self._older} {self._DELIMITER} {self._newer}"

    def __eq__(self, other: "Substitution") -> bool:
        return self._older == other._older and self._newer == other._newer

    @classmethod
    @cache
    def specialize(cls, valueClass):
        """Returns a subclass of Substitution that contains values of the given type."""
        name = valueClass.__name__ + cls.__name__
        return type(
            name,
            (cls,),
            {
                "__module__": cls.__module__,
                "_VALUE_TYPE": valueClass,
            },
        )

    @classmethod
    def fromString(cls, input: str):
        older, input = cls._VALUE_TYPE.fromString(input)
        input = re.sub(r"^\s*" + re.escape(cls._DELIMITER) + r"\s*", "", input)
        newer, input = cls._VALUE_TYPE.fromString(input)
        return cls(older, newer), input
