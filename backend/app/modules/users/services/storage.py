import os
import uuid
import io
from fastapi import UploadFile, status
from PIL import Image
from app.shared.exceptions import AppException
import logging

logger = logging.getLogger("app")

class BaseStorageService:
    async def upload_avatar(self, user_id: uuid.UUID, file: UploadFile) -> str:
        """Upload avatar and return the accessible URL."""
        raise NotImplementedError()

class LocalStorageService(BaseStorageService):
    def __init__(self, upload_dir: str = "static/avatars"):
        self.upload_dir = upload_dir
        os.makedirs(self.upload_dir, exist_ok=True)

    async def upload_avatar(self, user_id: uuid.UUID, file: UploadFile) -> str:
        # Validate extension
        allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}
        _, ext = os.path.splitext(file.filename or "")
        ext = ext.lower()
        if ext not in allowed_extensions:
            raise AppException(
                "Invalid file type. Allowed types: jpg, jpeg, png, webp",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # Validate size (max 5 MB)
        file.file.seek(0, os.SEEK_END)
        size = file.file.tell()
        file.file.seek(0)

        if size > 5 * 1024 * 1024:
            raise AppException(
                "File size exceeds 5 MB limit",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Read contents
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))

            # Resize/thumbnail (retaining aspect ratio, max 512x512)
            image.thumbnail((512, 512), Image.Resampling.LANCZOS)

            # Generate unique filename
            new_filename = f"{user_id}_{uuid.uuid4().hex}.jpg"
            target_path = os.path.join(self.upload_dir, new_filename)

            # Convert to RGB mode if necessary for JPEG format
            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")

            image.save(target_path, "JPEG", quality=85)
            logger.info(f"Successfully saved and compressed avatar to: {target_path}")

            return f"/static/avatars/{new_filename}"
        except AppException:
            raise
        except Exception as e:
            logger.error(f"Error processing avatar upload: {str(e)}", exc_info=True)
            raise AppException(
                "Could not process image file",
                status_code=status.HTTP_400_BAD_REQUEST
            )

storage_service = LocalStorageService()
