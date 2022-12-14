from abc import ABC, abstractmethod
from uuid import UUID
from .commontypes import Pair, Model

# from .component import Component


class Intersection:
    def __init__(self):
        self.added = {}
        self.deleted = {}
        self.common = {}


class Table(ABC):
    """Specifies how to retrieve components from, add them to, and delete them from a model."""

    @abstractmethod
    def getComponent(self, model: Model, id: UUID):
        """Retrieves the component with the given ID."""

    @abstractmethod
    def allComponents(self, model: Model) -> "Iterable[Component]":
        """Retrieves the complete set of components in the table."""

    @staticmethod
    @abstractmethod
    def getComponentId(component: "Component"):
        """Returns the unique ID of a component."""

    @staticmethod
    @abstractmethod
    def setComponentId(component: "Component", id: UUID):
        """Sets the unique ID of a component."""

    def intersect(self, models: Pair[Model]) -> Intersection:
        """Determines which components have been removed from the older model,
        which ones have been added to the newer model, and which ones appear in both."""
        intersection = Intersection()

        for component in self.allComponents(models[0]):
            id = self.getComponentId(component)
            intersection.deleted[id] = component

        for component in self.allComponents(models[1]):
            id = self.getComponentId(component)

            if id in intersection.deleted:
                intersection.common[id] = (intersection.deleted[id], component)
                del intersection.deleted[id]
            else:
                intersection.added[id] = component

        return intersection

    @abstractmethod
    def addComponent(self, component: "Component", model: Model):
        """Adds the given component to the table in the given model."""

    @abstractmethod
    def deleteComponent(self, component: "Component", model: Model):
        """Removes the given component from the table in the given model."""
