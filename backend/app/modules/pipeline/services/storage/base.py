from abc import ABC, abstractmethod

class BaseDocumentStorage(ABC):
    @abstractmethod
    def save(self, file_name: str, content: bytes) -> str:
        """Saves file content and returns its saved path/URI."""
        pass

    @abstractmethod
    def read(self, file_path: str) -> bytes:
        """Reads file content from the path/URI."""
        pass

    @abstractmethod
    def exists(self, file_path: str) -> bool:
        """Checks if a file exists at the given path/URI."""
        pass
