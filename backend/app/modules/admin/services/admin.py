import logging
from sqlalchemy.orm import Session
from sqlalchemy import func
import uuid
import datetime
from typing import Optional, List, Tuple, Dict, Any

from app.modules.users.models import User
from app.modules.users.models.activity import UserActivity
from app.modules.ipos.models import IPO, IPODetail
from app.modules.ai.models.analysis import AIAnalysis
from app.modules.watchlist.models.watchlist import WatchlistItem
from app.modules.users.repositories import user_repository
from app.modules.users.repositories.activity import user_activity_repository
from app.modules.admin.schemas.admin import AdminUserUpdatePayload
from app.shared.exceptions import AppException
from fastapi import status

logger = logging.getLogger("app")

class AdminService:
    def get_dashboard_analytics(self, db: Session) -> Dict[str, Any]:
        """
        Retrieves aggregated dashboard statistics and telemetry metrics.
        """
        total_users = db.query(User).count()
        total_ipos = db.query(IPO).count()
        total_watchlist_items = db.query(WatchlistItem).filter(WatchlistItem.deleted_at.is_(None)).count()
        total_ai_analyses = db.query(AIAnalysis).count()

        # Signups in last 30 days
        thirty_days_ago = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=30)
        # Use func.date for compatibility with SQLite (testing) and PostgreSQL (production)
        signup_query = db.query(
            func.date(User.created_at).label("day"),
            func.count(User.id).label("count")
        ).filter(
            User.created_at >= thirty_days_ago
        ).group_by(
            func.date(User.created_at)
        ).order_by(
            func.date(User.created_at)
        ).all()

        recent_signups = [{"date": str(row.day), "count": row.count} for row in signup_query]

        # Recent activities (audit logs)
        recent_activities = db.query(UserActivity).order_by(
            UserActivity.created_at.desc()
        ).limit(10).all()

        return {
            "total_users": total_users,
            "total_ipos": total_ipos,
            "total_watchlist_items": total_watchlist_items,
            "total_ai_analyses": total_ai_analyses,
            "recent_signups": recent_signups,
            "recent_activities": recent_activities
        }

    def list_users(
        self,
        db: Session,
        search: Optional[str] = None,
        role: Optional[str] = None,
        is_active: Optional[bool] = None,
        limit: int = 20,
        offset: int = 0
    ) -> Tuple[List[User], int]:
        """
        Queries and filters users list.
        """
        query = db.query(User)

        if search:
            query = query.filter(
                (User.full_name.ilike(f"%{search}%")) | (User.email.ilike(f"%{search}%"))
            )
        if role:
            query = query.filter(User.role == role)
        if is_active is not None:
            query = query.filter(User.is_active == is_active)

        total = query.count()
        results = query.order_by(User.created_at.desc()).offset(offset).limit(limit).all()
        return results, total

    def update_user(
        self,
        db: Session,
        admin_user_id: uuid.UUID,
        target_user_id: uuid.UUID,
        payload: AdminUserUpdatePayload
    ) -> User:
        """
        Updates target user role and status with safety assertions.
        """
        target_user = user_repository.get_by_id(db, target_user_id)
        if not target_user:
            raise AppException("User not found", status_code=status.HTTP_404_NOT_FOUND)

        # 1. Protect against self-deactivation
        if target_user_id == admin_user_id and payload.is_active is False:
            raise AppException("Cannot deactivate your own account", status_code=status.HTTP_400_BAD_REQUEST)

        # 2. Protect against self-downgrade
        if target_user_id == admin_user_id and payload.role == "USER":
            raise AppException("Cannot downgrade your own ADMIN role", status_code=status.HTTP_400_BAD_REQUEST)

        # 3. Protect against last active admin removal
        # If downgrading or deactivating a target admin, check if they are the last active admin
        target_is_active_admin = (target_user.role == "ADMIN" and target_user.is_active)
        changing_role_away = (payload.role is not None and payload.role != "ADMIN")
        deactivating = (payload.is_active is False)

        if target_is_active_admin and (changing_role_away or deactivating):
            active_admins_count = db.query(User).filter(User.role == "ADMIN", User.is_active == True).count()
            if active_admins_count <= 1:
                raise AppException("Cannot deactivate or demote the last active ADMIN account", status_code=status.HTTP_400_BAD_REQUEST)

        # Apply Updates & log specific admin actions
        if payload.full_name is not None:
            target_user.full_name = payload.full_name
            user_activity_repository.log_activity(
                db,
                user_id=admin_user_id,
                action="ADMIN_USER_UPDATED",
                metadata_json={"target_user_id": str(target_user_id), "field": "full_name"}
            )

        if payload.role is not None and payload.role != target_user.role:
            old_role = target_user.role
            target_user.role = payload.role
            user_activity_repository.log_activity(
                db,
                user_id=admin_user_id,
                action="ADMIN_USER_ROLE_CHANGED",
                metadata_json={
                    "target_user_id": str(target_user_id),
                    "old_role": old_role,
                    "new_role": payload.role
                }
            )

        if payload.is_active is not None and payload.is_active != target_user.is_active:
            target_user.is_active = payload.is_active
            act = "ADMIN_USER_REACTIVATED" if payload.is_active else "ADMIN_USER_DEACTIVATED"
            user_activity_repository.log_activity(
                db,
                user_id=admin_user_id,
                action=act,
                metadata_json={"target_user_id": str(target_user_id)}
            )

        target_user.updated_at = datetime.datetime.now(datetime.timezone.utc)
        db.commit()
        db.refresh(target_user)
        return target_user

    def deactivate_user_account(
        self,
        db: Session,
        admin_user_id: uuid.UUID,
        target_user_id: uuid.UUID
    ) -> User:
        """
        Deactivates a user (account deactivation instead of hard-delete).
        """
        target_user = user_repository.get_by_id(db, target_user_id)
        if not target_user:
            raise AppException("User not found", status_code=status.HTTP_404_NOT_FOUND)

        if target_user_id == admin_user_id:
            raise AppException("Cannot deactivate/delete your own account", status_code=status.HTTP_400_BAD_REQUEST)

        # Check if they are the last active admin
        if target_user.role == "ADMIN" and target_user.is_active:
            active_admins_count = db.query(User).filter(User.role == "ADMIN", User.is_active == True).count()
            if active_admins_count <= 1:
                raise AppException("Cannot deactivate the last active ADMIN account", status_code=status.HTTP_400_BAD_REQUEST)

        target_user.is_active = False
        target_user.updated_at = datetime.datetime.now(datetime.timezone.utc)
        
        user_activity_repository.log_activity(
            db,
            user_id=admin_user_id,
            action="ADMIN_USER_DEACTIVATED",
            metadata_json={"target_user_id": str(target_user_id), "reason": "Administrative deletion action"}
        )

        db.commit()
        db.refresh(target_user)
        return target_user

    def trigger_ai_analysis(
        self,
        db: Session,
        admin_user_id: uuid.UUID,
        ipo_id: uuid.UUID
    ) -> AIAnalysis:
        """
        Triggers manual AI analysis with duplicate request / cooldown rate limit check.
        """
        # Validate IPO exists
        ipo = db.query(IPO).filter(IPO.id == ipo_id).first()
        if not ipo:
            raise AppException("IPO not found", status_code=status.HTTP_404_NOT_FOUND)

        # 1. Protection Check (5-minute cooldown)
        now = datetime.datetime.now(datetime.timezone.utc)
        latest_analysis = db.query(AIAnalysis).filter(
            AIAnalysis.ipo_id == ipo_id
        ).order_by(AIAnalysis.created_at.desc()).first()

        if latest_analysis:
            created_at = latest_analysis.created_at
            if created_at.tzinfo is None:
                created_at = created_at.replace(tzinfo=datetime.timezone.utc)
            diff = (now - created_at).total_seconds()
            if diff < 300:
                raise AppException(
                    f"AI regeneration cooldown active. Please wait {int(300 - diff)} seconds.",
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS
                )

        # 2. Trigger via existing AI Analysis Service
        from app.modules.ai.services.analysis import ai_analysis_service
        analysis = ai_analysis_service.generate_analysis(db, ipo_id=ipo_id, force_regenerate=True)

        # 3. Log Audit Activity
        user_activity_repository.log_activity(
            db,
            user_id=admin_user_id,
            action="ADMIN_AI_TRIGGERED",
            metadata_json={"ipo_id": str(ipo_id), "analysis_id": str(analysis.id)}
        )

        return analysis

admin_service = AdminService()
