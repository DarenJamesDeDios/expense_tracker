from abc import ABC, abstractmethod

class BaseTheme(ABC):
    @abstractmethod
    def apply(self, root):
        pass