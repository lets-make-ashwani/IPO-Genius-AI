from sqlalchemy.orm import Session
from typing import Optional, List, Tuple
import uuid
import logging
from datetime import datetime, timezone


from app.modules.watchlist.models.watchlist import WatchlistFolder, WatchlistItem, WatchlistPriority
from app.modules.watchlist.repositories.watchlist import watchlist_repository
from app.modules.watchlist.schemas.watchlist import WatchlistItemCreate, WatchlistItemUpdate, WatchlistSummaryResponse
from app.modules.ipos.services.ipo import ipo_service
from app.modules.ai.repositories.analysis import ai_analysis_repository
from app.modules.users.repositories.activity import user_activity_repository
from app.shared.exceptions import AppException
from fastapi import status

logger = logging.getLogger("app")

class WatchlistService:
    def get_or_create_default_folder(self, db: Session, user_id: uuid.UUID) -> WatchlistFolder:
        folder = watchlist_repository.get_default_folder(db, user_id)
        if not folder:
            logger.info(f"Creating default watchlist folder for user: {user_id}")
            folder = WatchlistFolder(
                id=uuid.uuid4(),
                user_id=user_id,
                name="Default",
                color="#000000",
                is_default=True
            )
            folder = watchlist_repository.create_folder(db, folder)
        return folder

    def get_user_folder(self, db: Session, user_id: uuid.UUID, folder_id: Optional[uuid.UUID] = None) -> WatchlistFolder:
        if folder_id:
            folder = watchlist_repository.get_folder_by_id(db, folder_id)
            if not folder:
                raise AppException("Watchlist folder not found", status_code=status.HTTP_404_NOT_FOUND)
            if folder.user_id != user_id:
                raise AppException("Access denied: Not your watchlist folder", status_code=status.HTTP_403_FORBIDDEN)
            return folder
        return self.get_or_create_default_folder(db, user_id)

    def add_to_watchlist(self, db: Session, user_id: uuid.UUID, item_in: WatchlistItemCreate) -> WatchlistItem:
        # 1. Resolve IPO
        ipo = ipo_service.get_ipo_by_id(db, item_in.ipo_id)
        if not ipo:
            raise AppException("IPO not found", status_code=status.HTTP_404_NOT_FOUND)

        # 2. Get Folder
        folder = self.get_user_folder(db, user_id, item_in.folder_id)

        # 3. Check duplicate active item
        existing = watchlist_repository.get_active_by_folder_and_ipo(db, folder.id, ipo.id)
        if existing:
            raise AppException("IPO already in watchlist", status_code=status.HTTP_400_BAD_REQUEST)

        # 4. Fetch AI Analysis Snapshot
        ai_analysis = ai_analysis_repository.get_active_by_ipo_id(db, ipo.id)
        ai_overall_score = ai_analysis.overall_score if ai_analysis else None
        ai_recommendation = ai_analysis.recommendation.value if ai_analysis else None
        ai_confidence_score = ai_analysis.confidence_score if ai_analysis else None

        # 5. Create Item
        item = WatchlistItem(
            id=uuid.uuid4(),
            folder_id=folder.id,
            ipo_id=ipo.id,
            notes=item_in.notes,
            tags=item_in.tags,
            priority=item_in.priority or WatchlistPriority.MEDIUM,
            reminder_enabled=item_in.reminder_enabled or False,
            reminder_date=item_in.reminder_date,
            ai_overall_score=ai_overall_score,
            ai_recommendation=ai_recommendation,
            ai_confidence_score=ai_confidence_score,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            ipo=ipo
        )
        item = watchlist_repository.create_item(db, item)

        # 6. Log Activity
        user_activity_repository.log_activity(
            db,
            user_id=user_id,
            action="WATCHLIST_ADD",
            metadata_json={"ipo_id": str(ipo.id), "company_name": ipo.company_name, "folder_id": str(folder.id)}
        )
        logger.info(f"User {user_id} added IPO {ipo.company_name} to watchlist folder {folder.name}")
        return item

    def update_watchlist_item(self, db: Session, user_id: uuid.UUID, item_id: uuid.UUID, update_in: WatchlistItemUpdate) -> WatchlistItem:
        item = watchlist_repository.get_item_by_id(db, item_id)
        if not item or item.deleted_at is not None:
            raise AppException("Watchlist item not found", status_code=status.HTTP_404_NOT_FOUND)
        
        # Verify ownership
        if item.folder.user_id != user_id:
            raise AppException("Access denied: Not your watchlist item", status_code=status.HTTP_403_FORBIDDEN)

        if update_in.notes is not None:
            item.notes = update_in.notes
        if update_in.tags is not None:
            item.tags = update_in.tags
        if update_in.priority is not None:
            item.priority = update_in.priority
        if update_in.reminder_enabled is not None:
            item.reminder_enabled = update_in.reminder_enabled
        if update_in.reminder_date is not None:
            item.reminder_date = update_in.reminder_date

        return watchlist_repository.update_item(db, item)

    def remove_from_watchlist(self, db: Session, user_id: uuid.UUID, ipo_id: uuid.UUID, folder_id: Optional[uuid.UUID] = None) -> None:
        folder = self.get_user_folder(db, user_id, folder_id)
        item = watchlist_repository.get_active_by_folder_and_ipo(db, folder.id, ipo_id)
        if not item:
            raise AppException("Watchlist item not found", status_code=status.HTTP_404_NOT_FOUND)

        watchlist_repository.soft_delete_item(db, item)

        # Log Activity
        user_activity_repository.log_activity(
            db,
            user_id=user_id,
            action="WATCHLIST_REMOVE",
            metadata_json={"ipo_id": str(ipo_id), "folder_id": str(folder.id)}
        )
        logger.info(f"User {user_id} removed IPO {ipo_id} from watchlist folder {folder.name}")

    def list_watchlist(
        self,
        db: Session,
        user_id: uuid.UUID,
        folder_id: Optional[uuid.UUID] = None,
        sort_by: str = "Newest",
        status_filter: Optional[str] = None,
        sector_filter: Optional[str] = None,
        industry_filter: Optional[str] = None,
        ipo_type_filter: Optional[str] = None,
        rec_filter: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> Tuple[List[WatchlistItem], int]:
        folder = self.get_user_folder(db, user_id, folder_id)
        limit = min(max(limit, 1), 100)
        offset = max(offset, 0)
        return watchlist_repository.list_active_by_folder(
            db,
            folder_id=folder.id,
            sort_by=sort_by,
            status_filter=status_filter,
            sector_filter=sector_filter,
            industry_filter=industry_filter,
            ipo_type_filter=ipo_type_filter,
            rec_filter=rec_filter,
            limit=limit,
            offset=offset
        )

    def get_summary(self, db: Session, user_id: uuid.UUID, folder_id: Optional[uuid.UUID] = None) -> WatchlistSummaryResponse:
        folder = self.get_user_folder(db, user_id, folder_id)
        total = watchlist_repository.count_active_by_folder(db, folder.id)
        dist = watchlist_repository.get_status_distribution(db, folder.id)
        
        return WatchlistSummaryResponse(
            total_count=total,
            upcoming_count=dist.get("Upcoming", 0),
            open_count=dist.get("Open", 0),
            closed_count=dist.get("Closed", 0),
            listed_count=dist.get("Listed", 0)
        )

    def get_count(self, db: Session, user_id: uuid.UUID, folder_id: Optional[uuid.UUID] = None) -> int:
        folder = self.get_user_folder(db, user_id, folder_id)
        return watchlist_repository.count_active_by_folder(db, folder.id)

watchlist_service = WatchlistService()
