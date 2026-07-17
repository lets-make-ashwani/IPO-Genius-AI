from sqlalchemy.orm import Session
from typing import Optional, List, Tuple
import uuid
import logging
from app.modules.ipos.models.ipo import IPO, IPOStatus, IPOType
from app.modules.ipos.repositories.ipo import ipo_repository
from app.shared.exceptions import AppException
from fastapi import status

logger = logging.getLogger("app")

class IPOService:
    def get_ipo_by_id(self, db: Session, ipo_id: uuid.UUID) -> IPO:
        ipo = ipo_repository.get_by_id(db, ipo_id)
        if not ipo:
            raise AppException("IPO not found", status_code=status.HTTP_404_NOT_FOUND)
        return ipo

    def get_ipo_by_slug(self, db: Session, slug: str) -> IPO:
        ipo = ipo_repository.get_by_slug(db, slug)
        if not ipo:
            raise AppException("IPO not found", status_code=status.HTTP_404_NOT_FOUND)
        return ipo

    def get_ipos(
        self,
        db: Session,
        ipo_status: Optional[IPOStatus] = None,
        ipo_type: Optional[IPOType] = None,
        search: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> Tuple[List[IPO], int]:
        # Enforce limits to protect database performance
        limit = min(max(limit, 1), 100)
        offset = max(offset, 0)

        logger.info(f"Fetching IPOs: status={ipo_status}, type={ipo_type}, search='{search}', limit={limit}, offset={offset}")
        return ipo_repository.get_ipos(
            db, status=ipo_status, ipo_type=ipo_type, search=search, limit=limit, offset=offset
        )

ipo_service = IPOService()
