from abc import ABC, abstractmethod
from uuid import UUID


class Session(ABC):
    """Allows"""

    @abstractmethod
    def ask(self, question: str):
        pass

    @abstractmethod
    def warn(self, message: str) -> None:
        pass

    @abstractmethod
    def fatal(self, message: str) -> None:
        pass

    @abstractmethod
    def setContext(self, componentType: str, componentID: UUID, property):
        pass
