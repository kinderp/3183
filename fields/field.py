from abc import ABC, abstractmethod

class Field(ABC):
    """
    Defined here interface for field types
    """
    @abstractmethod
    def render(self):
        pass

