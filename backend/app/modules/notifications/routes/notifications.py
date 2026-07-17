from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
import uuid

from app.database.session import get_db
from app.shared.dependencies import get_current_user
from app.modules.users.models.user import User
from app.modules.notifications.schemas.notification import (
    NotificationResponse,
    NotificationPreferenceResponse,
    NotificationPreferenceUpdate,
)
from app.modules.notifications.models.notification import NotificationStatus
from app.modules.notifications.services.notification import notification_service

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("", response_model=dict)
def get_notifications(
    notification_status: Optional[NotificationStatus] = Query(None, alias="status"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    results, total = notification_service.list_notifications(
        db, user_id=current_user.id, status_filter=notification_status, limit=limit, offset=offset
    )
    return {
        "success": True,
        "message": "Notifications retrieved successfully",
        "data": [NotificationResponse.model_validate(n) for n in results],
        "meta": {
            "total": total,
            "limit": limit,
            "offset": offset
        }
    }

@router.get("/count", response_model=dict)
def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    count = notification_service.get_unread_count(db, user_id=current_user.id)
    return {
        "success": True,
        "message": "Unread count retrieved successfully",
        "data": {
            "count": count
        }
    }

@router.put("/{notification_id}/read", response_model=dict)
def mark_as_read(
    notification_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    notification = notification_service.mark_as_read(db, user_id=current_user.id, notification_id=notification_id)
    return {
        "success": True,
        "message": "Notification marked as read successfully",
        "data": NotificationResponse.model_validate(notification)
    }

@router.post("/read-all", response_model=dict)
def mark_all_as_read(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    rows = notification_service.mark_all_as_read(db, user_id=current_user.id)
    return {
        "success": True,
        "message": f"Successfully marked {rows} notifications as read"
    }

@router.get("/preferences", response_model=dict)
def get_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    pref = notification_service.get_preferences(db, user_id=current_user.id)
    return {
        "success": True,
        "message": "Notification preferences retrieved successfully",
        "data": NotificationPreferenceResponse.model_validate(pref)
    }

@router.put("/preferences", response_model=dict)
def update_preferences(
    payload: NotificationPreferenceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    pref = notification_service.update_preferences(db, user_id=current_user.id, update_in=payload)
    return {
        "success": True,
        "message": "Notification preferences updated successfully",
        "data": NotificationPreferenceResponse.model_validate(pref)
    }
