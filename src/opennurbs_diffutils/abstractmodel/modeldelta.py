from pathlib import Path
from typing import TextIO, Tuple

from .commontypes import Model, Pair
from .componentdelta import (
    ComponentDelta,
    ComponentModification,
    ComponentAddition,
    ComponentDeletion,
)
from .error import ParseError
from .filedescription import FileDescription
from .modeltype import ModelType
from .propertymap import PropertyValueMap, PropertyDeltaMap
from .session import Session


OLDER_FILE_PREFIX = "---"
NEWER_FILE_PREFIX = "+++"


class ModelDelta:
    """Describes the differences between two version of a model."""

    def __init__(self, type: ModelType):
        self.type = type
        """The type of model."""

        self.files: Tuple[FileDescription, FileDescription]
        """The files that were diffed to create the delta."""

        self.properties = PropertyDeltaMap()
        """The properties of the model that were changed."""

        self.additions: list[ComponentAddition] = []
        """The list of components that were added to the model."""

        self.deletions: list[ComponentDeletion] = []
        """The list of components that were removed from the model."""

        self.modifications: list[ComponentModification] = []
        """The list of components that were removed from the model."""

    @property
    def components(self):
        """Returns the list of components that were added, removed, or modified."""
        yield from self.additions
        yield from self.modifications
        yield from self.deletions

    @property
    def hasDifferences(self):
        """Returns true if the object describes at least one change."""
        return (
            len(self.properties) > 0
            or len(self.additions) > 0
            or len(self.deletions) > 0
            or len(self.modifications) > 0
        )

    def setFilePaths(self, paths: Pair[Path]):
        self.files = Pair((FileDescription(paths[0]), FileDescription(paths[1])))

    def writeHeader(self, output: TextIO):
        output.write(f"{OLDER_FILE_PREFIX} {self.files[0]}\n")
        output.write(f"{NEWER_FILE_PREFIX} {self.files[1]}\n")

    def write(self, output: TextIO):
        """Writes the delta to the given output stream."""
        self.writeHeader(output)
        self.properties.write(output)
        for component in self.components:
            component.write(output)

    def readHeader(self, input: TextIO):
        desc1, prefix1 = FileDescription.fromString(input.readline())
        desc2, prefix2 = FileDescription.fromString(input.readline())
        if (
            desc1
            and desc2
            and prefix1 == OLDER_FILE_PREFIX
            and prefix2 == NEWER_FILE_PREFIX
        ):
            self.files = (desc1, desc2)

    def read(self, input: TextIO):
        """Reads a delta from the given input stream."""
        self.readHeader(input)
        current = None
        lineNumber = 3  # file starts at line 1; header is 2 lines
        for line in input:

            try:
                if line.startswith("@@"):
                    current = ComponentDelta.fromHeader(line, self.type.componentTypes)
                    if isinstance(current, ComponentAddition):
                        self.additions.append(current)
                    elif isinstance(current, ComponentDeletion):
                        self.deletions.append(current)
                    else:
                        self.modifications.append(current)
                elif current:
                    current.readline(line)
                else:
                    self.properties.readline(line, self.type)

            except:
                raise ParseError(lineNumber)

            lineNumber += 1

    def apply(self, model: Model, session: Session):
        """Applies the changes described in the delta to the given model."""
        self.properties.apply(model, session)
        for delta in self.components:
            delta.apply(model, session)

    def compare(self, files: Pair[Model], session: Session):
        """Finds differences between the given pair of models."""
        self.properties = PropertyDeltaMap.fromDifferences(
            files, self.type.properties, session
        )
        for table in self.type.tables:
            intersection = table.intersect(files)

            for uuid, entities in intersection.common.items():
                try:
                    componentType = self.type.componentTypes.fromInstance(entities[0])
                    # TODO: Handle case where object types are different
                    delta = ComponentModification(componentType, uuid)
                    delta.properties = PropertyDeltaMap.fromDifferences(
                        entities, componentType.properties, session
                    )
                    if len(delta.properties) > 0:
                        self.modifications.append(delta)
                except KeyError as err:
                    session.warn(str(err))

            for uuid, component in intersection.added.items():
                try:
                    componentType = self.type.componentTypes.fromInstance(component)
                    default = componentType.create(component.model)
                    delta = ComponentAddition(componentType, uuid)
                    delta.properties = PropertyValueMap.fromNonDefaultValues(
                        componentType.properties, component, default
                    )
                    self.additions.append(delta)
                except KeyError as err:
                    session.warn(str(err))

            for uuid, component in intersection.deleted.items():
                try:
                    componentType = self.type.componentTypes.fromInstance(component)
                    default = componentType.create(component.model)
                    delta = ComponentDeletion(componentType, uuid)
                    delta.properties = PropertyValueMap.fromNonDefaultValues(
                        componentType.properties, component, default
                    )
                    self.deletions.append(delta)
                except KeyError as err:
                    session.warn(str(err))

    def reverse(self):
        """Returns a delta that has the opposite meaning of this one."""
        reversed = self.__class__(self.type)
        reversed.files = (self.files[1], self.files[0])
        reversed.properties = self.properties.reverse()
        reversed.additions = self.deletions
        reversed.deletions = self.additions
        for delta in self.modifications:
            reversed.modifications.append(delta.reverse())
        return reversed

    def findComponent(self, id):
        """Searches for a ComponentDelta with the given ID."""
        for component in self.components:
            if component.id == id:
                return component
        return None

    def merge(self, other, session):
        """Returns a delta that contains both the changes described in this delta as well as those described in another."""
        merged = self.__class__(self.type)
        merged.files = self.files  # temp
        merged.properties = self.properties.merge(other.properties)

        for delta in self.components:
            otherDelta = other.findComponent(delta.id)
            if otherDelta:
                merged.addComponent(delta.merge(otherDelta, session))
            else:
                merged.addComponent(delta)

        for otherDelta in other.components:
            if not self.findComponent(otherDelta.id):
                merged.addComponent(otherDelta)

        return merged

    def addComponent(self, component):
        """Adds a component to the delta."""
        if isinstance(component, ComponentAddition):
            self.additions.append(component)
        elif isinstance(component, ComponentDeletion):
            self.deletions.append(component)
        elif isinstance(component, ComponentModification):
            self.modifications.append(component)
        else:
            raise Exception("Invalid component type")
