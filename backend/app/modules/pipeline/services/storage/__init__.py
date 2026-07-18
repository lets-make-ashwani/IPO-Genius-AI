from app.modules.pipeline.services.storage.base import BaseDocumentStorage
from app.modules.pipeline.services.storage.local import LocalDocumentStorage

def get_document_storage() -> BaseDocumentStorage:
    from app.config.settings import settings
    # Right now we only support LOCAL
    if settings.DOCUMENT_STORAGE_TYPE.upper() == "LOCAL":
        return LocalDocumentStorage(base_dir=settings.DOCUMENT_STORAGE_PATH)
    raise ValueError(f"Unknown document storage type: {settings.DOCUMENT_STORAGE_TYPE}")
