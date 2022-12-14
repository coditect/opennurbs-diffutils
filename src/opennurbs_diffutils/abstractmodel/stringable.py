from abc import ABC, abstractmethod
from typing import Tuple


class Stringable(ABC):
    """An object that can be converted to and from a textual representation."""

    @abstractmethod
    def __str__(self) -> str:
        """Produces a textual representation of the object."""

    @classmethod
    @abstractmethod
    def fromString(cls, input: str) -> "Tuple[Self, str]":
        """Attempts to parses an object from the beginning of the given string.

        Any part of the string that follows the parsed textual representation is returned."""
