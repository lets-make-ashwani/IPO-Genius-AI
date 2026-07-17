from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, asc, func
from typing import Optional, List, Tuple
import uuid
from datetime import datetime, timezone
from app.modules.watchlist.models.watchlist import WatchlistFolder, WatchlistItem
from app.modules.ipos.models.ipo import IPO

class WatchlistRepository:
    def get_default_folder(self, db: Session, user_id: uuid.UUID) -> Optional[WatchlistFolder]:
        return (
            db.query(WatchlistFolder)
            .filter(WatchlistFolder.user_id == user_id, WatchlistFolder.is_default == True)
            .first()
        )

    def get_folder_by_id(self, db: Session, folder_id: uuid.UUID) -> Optional[WatchlistFolder]:
        return (
            db.query(WatchlistFolder)
            .filter(WatchlistFolder.id == folder_id)
            .first()
        )

    def create_folder(self, db: Session, folder: WatchlistFolder) -> WatchlistFolder:
        db.add(folder)
        db.commit()
        db.refresh(folder)
        return folder

    def get_item_by_id(self, db: Session, item_id: uuid.UUID) -> Optional[WatchlistItem]:
        return (
            db.query(WatchlistItem)
            .options(joinedload(WatchlistItem.ipo), joinedload(WatchlistItem.folder))
            .filter(WatchlistItem.id == item_id)
            .first()
        )

    def get_active_by_folder_and_ipo(self, db: Session, folder_id: uuid.UUID, ipo_id: uuid.UUID) -> Optional[WatchlistItem]:
        return (
            db.query(WatchlistItem)
            .filter(
                WatchlistItem.folder_id == folder_id,
                WatchlistItem.ipo_id == ipo_id,
                WatchlistItem.deleted_at == None
            )
            .first()
        )

    def list_active_by_folder(
        self,
        db: Session,
        folder_id: uuid.UUID,
        sort_by: str = "Newest",
        status_filter: Optional[str] = None,
        sector_filter: Optional[str] = None,
        industry_filter: Optional[str] = None,
        ipo_type_filter: Optional[str] = None,
        rec_filter: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> Tuple[List[WatchlistItem], int]:
        query = (
            db.query(WatchlistItem)
            .join(IPO, WatchlistItem.ipo_id == IPO.id)
            .options(joinedload(WatchlistItem.ipo))
            .filter(WatchlistItem.folder_id == folder_id, WatchlistItem.deleted_at == None)
        )

        # Filters
        if status_filter:
            query = query.filter(IPO.status == status_filter)
        if sector_filter:
            query = query.filter(IPO.sector.ilike(f"%{sector_filter}%"))
        if industry_filter:
            query = query.filter(IPO.industry.ilike(f"%{industry_filter}%"))
        if ipo_type_filter:
            query = query.filter(IPO.ipo_type == ipo_type_filter)
        if rec_filter:
            query = query.filter(WatchlistItem.ai_recommendation == rec_filter)

        # Sorting
        if sort_by == "Newest":
            query = query.order_by(desc(WatchlistItem.created_at))
        elif sort_by == "Oldest":
            query = query.order_by(asc(WatchlistItem.created_at))
        elif sort_by == "AI Score":
            query = query.order_by(desc(WatchlistItem.ai_overall_score))
        elif sort_by == "IPO Opening Date":
            query = query.order_by(desc(IPO.open_date))
        elif sort_by == "Company Name":
            query = query.order_by(asc(IPO.company_name))
        else:
            query = query.order_by(desc(WatchlistItem.created_at))

        total = query.count()
        results = query.offset(offset).limit(limit).all()

        return results, total

    def count_active_by_folder(self, db: Session, folder_id: uuid.UUID) -> int:
        return (
            db.query(func.count(WatchlistItem.id))
            .filter(WatchlistItem.folder_id == folder_id, WatchlistItem.deleted_at == None)
            .scalar() or 0
        )

    def get_status_distribution(self, db: Session, folder_id: uuid.UUID) -> dict:
        results = (
            db.query(IPO.status, func.count(WatchlistItem.id))
            .join(WatchlistItem, WatchlistItem.ipo_id == IPO.id)
            .filter(WatchlistItem.folder_id == folder_id, WatchlistItem.deleted_at == None)
            .group_by(IPO.status)
            .all()
        )
        dist = {status_val: count for status_val, count in results}
        return dist

    def create_item(self, db: Session, item: WatchlistItem) -> WatchlistItem:
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    def update_item(self, db: Session, item: WatchlistItem) -> WatchlistItem:
        db.commit()
        db.refresh(item)
        return item

    def soft_delete_item(self, db: Session, item: WatchlistItem) -> WatchlistItem:
        item.deleted_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(item)
        return item

watchlist_repository = WatchlistRepository()
