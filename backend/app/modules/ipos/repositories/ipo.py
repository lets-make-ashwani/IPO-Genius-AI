from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, desc
from typing import Optional, List, Tuple
import uuid
from app.modules.ipos.models.ipo import IPO, IPOStatus, IPOType
from app.modules.ipos.models.detail import IPODetail

class IPORepository:
    def get_by_id(self, db: Session, ipo_id: uuid.UUID) -> Optional[IPO]:
        return (
            db.query(IPO)
            .options(joinedload(IPO.details))
            .filter(IPO.id == ipo_id)
            .first()
        )

    def get_by_slug(self, db: Session, slug: str) -> Optional[IPO]:
        return (
            db.query(IPO)
            .options(joinedload(IPO.details))
            .filter(IPO.slug == slug)
            .first()
        )

    def get_ipos(
        self,
        db: Session,
        status: Optional[IPOStatus] = None,
        ipo_type: Optional[IPOType] = None,
        search: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> Tuple[List[IPO], int]:
        query = db.query(IPO).options(joinedload(IPO.details))

        if status is not None:
            query = query.filter(IPO.status == status.value)
        
        if ipo_type is not None:
            query = query.filter(IPO.ipo_type == ipo_type.value)

        if search is not None and search.strip() != "":
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    IPO.company_name.ilike(search_pattern),
                    IPO.sector.ilike(search_pattern),
                    IPO.industry.ilike(search_pattern)
                )
            )

        total = query.count()
        results = (
            query.order_by(desc(IPO.open_date))
            .offset(offset)
            .limit(limit)
            .all()
        )

        return results, total

ipo_repository = IPORepository()
