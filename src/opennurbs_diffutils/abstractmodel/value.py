from abc import abstractmethod
import json
import re
from typing import Any, Generic, Type, TypeVar
import uuid
from .delta import Substitution
from .stringable import Stringable


T = TypeVar("T")


class Value(Stringable, Generic[T]):
    """Holds a piece of information that was retrieved from or that can be assigned to a component property."""

    __slots__ = "value"

    def __init__(self, value: T):
        # whatever comes out of the accessor is passed into here
        self.value = value

    def __repr__(self):
        """Produces a textual representation of the value to be used during development."""
        return f"{self.__class__.__qualname__}({self})"

    def __str__(self) -> str:
        """Produces a textual representation of the value."""
        return str(self.value)

    def __eq__(self, other: "Value[T]") -> bool:
        """Compares this value to another and returns true if they are equal."""
        return self.value == other.value

    def diff(self, newer: "Value[T]"):
        """Returns an instance of Delta that describes how this value can be transformed into another."""
        return Substitution(self, newer)

    @classmethod
    def deltaType(cls):
        """Returns the subclass of Delta returned by the diff method."""
        return Substitution.specialize(cls)


# UUID_Set = CollectionCodec("set of UUIDs", UUID, set)


class JSONEncodeableValue(Value):
    """An implementation of Value that uses the json package to convert values to and from their textual representations."""

    _DECODER = json.JSONDecoder(strict=False)
    _EXPECTED_TYPE = object
    _LABEL = ""

    def __str__(self):
        return json.dumps(self.value)

    @classmethod
    def fromString(cls, input):
        value, end = cls._DECODER.raw_decode(input)
        if not isinstance(value, cls._EXPECTED_TYPE):
            raise Exception(f"'{input}' is not a valid {cls._LABEL}")
        return cls(value), input[end:]

    @classmethod
    def defineSubclass(
        cls, name: str, label: str, expected_type
    ) -> "Type[JSONEncodeableValue]":
        """Returns a subclass of JSONEncodeableValue that parses values of a specific type."""
        return type(
            name,
            (cls,),
            {
                "__module__": cls.__module__,
                "_LABEL": label,
                "_EXPECTED_TYPE": expected_type,
            },
        )


BooleanValue = JSONEncodeableValue.defineSubclass("BooleanValue", "boolean", bool)
FloatValue = JSONEncodeableValue.defineSubclass("FloatValue", "float", float)
IntegerValue = JSONEncodeableValue.defineSubclass("IntegerValue", "integer", int)
StringValue = JSONEncodeableValue.defineSubclass("StringValue", "string", str)


class RegexParseableValue(Value):
    """An implementation of Value that parses values from a string using a regular expression."""

    _LABEL: str
    _PATTERN: re.Pattern

    @classmethod
    def fromString(cls, raw):
        match = cls._PATTERN.match(raw)
        if not match:
            raise Exception(f"'{raw}' is not a valid {cls._LABEL}")
        return cls(cls._createValueFromMatch(match)), raw[match.end() :]

    @staticmethod
    @abstractmethod
    def _createValueFromMatch(match: re.Match):
        """Creates an instance of an object from the given Match object."""


class UUIDValue(RegexParseableValue):
    """An implementation of Value that stores UUIDs."""

    _PATTERN = re.compile(
        r"\s*([0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12})",
        re.IGNORECASE,
    )

    @staticmethod
    def _createValueFromMatch(match):
        return uuid.UUID(match[1])


class EnumeratedValue(Value):
    """An implementation of Value that maps members of an enumeration to their textual representations."""

    _LABEL = ""
    _VALUES_TO_STRINGS = {}
    _STRINGS_TO_VALUES = {}

    def __str__(self):
        return self._VALUES_TO_STRINGS[self.value]

    @classmethod
    def fromString(cls, input):
        match = re.match(r"\s*(\w+)", input)
        if not match:
            raise Exception(f"unable to parse token from {input}")
        try:
            value = cls._STRINGS_TO_VALUES[match[1].casefold()]
            return cls(value), input[match.end() :]
        except:
            raise Exception(f"{match[1]} is not a valid {cls._LABEL}")

    @classmethod
    def defineSubclass(cls, name: str, label: str, translation_table: dict[Any, str]):
        """Returns a subclass of EnumeratedValue that uses  the given mapping to tranlate between values and strings."""
        return type(
            name,
            (cls,),
            {
                "__module__": cls.__module__,
                "_LABEL": label,
                "_VALUES_TO_STRINGS": translation_table,
                "_STRINGS_TO_VALUES": {
                    label.casefold(): value
                    for value, label in translation_table.items()
                },
            },
        )
