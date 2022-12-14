from typing import TypeVar, TypeAlias

# Component: TypeAlias = object
# "A component in a 3D model"

Model: TypeAlias = object
"A 3D model"

T = TypeVar("T")
Pair = tuple[T, T]
