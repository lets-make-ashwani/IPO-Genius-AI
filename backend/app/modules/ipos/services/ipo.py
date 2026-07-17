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

    def create_ipo(self, db: Session, ipo_data) -> IPO:
        # Date validation
        if ipo_data.open_date > ipo_data.close_date:
            raise AppException("Open date must be before or equal to close date", status_code=status.HTTP_400_BAD_REQUEST)

        # Generate unique slug
        import re
        slug = ipo_data.slug
        if not slug:
            base_slug = ipo_data.company_name.lower()
            base_slug = re.sub(r'[^a-z0-9\s-]', '', base_slug)
            base_slug = re.sub(r'[\s-]+', '-', base_slug)
            base_slug = base_slug.strip('-')
            
            slug = base_slug
            counter = 1
            while db.query(IPO).filter(IPO.slug == slug).first():
                slug = f"{base_slug}-{counter}"
                counter += 1

        logger.info(f"Creating new IPO: '{ipo_data.company_name}' with slug: '{slug}'")
        return ipo_repository.create(db, ipo_data, slug)

    def update_ipo(self, db: Session, ipo_id: uuid.UUID, ipo_data) -> IPO:
        ipo = self.get_ipo_by_id(db, ipo_id)

        # Date validation
        new_open = ipo_data.open_date if ipo_data.open_date is not None else ipo.open_date
        new_close = ipo_data.close_date if ipo_data.close_date is not None else ipo.close_date
        if new_open > new_close:
            raise AppException("Open date must be before or equal to close date", status_code=status.HTTP_400_BAD_REQUEST)

        logger.info(f"Updating IPO: {ipo_id}")
        return ipo_repository.update(db, ipo, ipo_data)

    def delete_ipo(self, db: Session, ipo_id: uuid.UUID) -> None:
        ipo = self.get_ipo_by_id(db, ipo_id)
        logger.info(f"Deleting IPO: {ipo_id}")
        ipo_repository.delete(db, ipo)

ipo_service = IPOService()

