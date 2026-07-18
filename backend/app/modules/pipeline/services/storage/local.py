import os
from app.modules.pipeline.services.storage.base import BaseDocumentStorage

class LocalDocumentStorage(BaseDocumentStorage):
    def __init__(self, base_dir: str = "./pipeline_docs"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def save(self, file_name: str, content: bytes) -> str:
        # Prevent path traversal
        clean_file_name = os.path.basename(file_name)
        file_path = os.path.join(self.base_dir, clean_file_name)
        with open(file_path, "wb") as f:
            f.write(content)
        return os.path.abspath(file_path)

    def read(self, file_path: str) -> bytes:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, "rb") as f:
            return f.read()

    def exists(self, file_path: str) -> bool:
        return os.path.exists(file_path)
