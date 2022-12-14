from abc import abstractmethod
from typing import Callable, Generic, TypeVar, Union


H = TypeVar("H")
V = TypeVar("V")


class Accessor(Generic[H, V]):
    """Describes how to get and set values of a specific object property."""

    @abstractmethod
    def get(self, host: H) -> V:
        """Get the value of a property from the given host object."""

    @abstractmethod
    def set(self, host: H, newValue: V) -> None:
        """Set the value of a property on the given host object."""


class PathAccessor(Accessor[H, V]):
    """An implementation of Accessor that traverses a dot-delimited path to get and set an object property."""

    __slots__ = "_path"

    def __init__(self, path: str):
        self._path = path.split(".")

    def __str__(self) -> str:
        return ".".join(self._path)

    def get(self, host: H) -> V:
        try:
            intermediate = host
            for name in self._path[:-1]:
                intermediate = getattr(intermediate, name)
            return getattr(intermediate, self._path[-1])
        except AttributeError as e:
            raise AttributeError(
                f"Unable to get {self} from object of type {host.__class__.__name__}: {e}"
            )

    def set(self, host: H, value: V) -> None:
        for name in self._path[:-1]:
            host = getattr(host, name)
        setattr(host, self._path[-1], value)

    @classmethod
    def ifString(cls, maybeAccessor: Union[Accessor, str]) -> Accessor:
        """Returns a PathAccessor based on the given parameter if that parameter is a string.

        If it is not, the parameter is returned unmodified."""
        return cls(maybeAccessor) if isinstance(maybeAccessor, str) else maybeAccessor


class FunctionalAccessor(Accessor[H, V]):
    """An implementation of Accessor that uses a pair of functions to get and set an object property."""

    __slots__ = ("get", "set")

    def __init__(self, getter: Callable[[H], V], setter: Callable[[H, V], None]):
        self.get = getter
        self.set = setter
