# Legacy
from abc import ABC, abstractmethod


class UserContent(ABC):
    @property
    @abstractmethod
    def key(self) -> str:
        pass

    # Markdown representation as a long string
    @property
    @abstractmethod
    def markdown_text(self) -> str:
        pass
