from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
import uuid

from app.database.session import get_db
from app.shared.dependencies import get_current_user
from app.modules.users.models.user import User
from app.modules.watchlist.schemas.watchlist import (
    WatchlistItemResponse,
    WatchlistItemCreate,
    WatchlistItemUpdate,
    WatchlistSummaryResponse,
)
from app.modules.watchlist.services.watchlist import watchlist_service

router = APIRouter(prefix="/watchlist", tags=["Watchlist"])

@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
def add_to_watchlist(
    payload: WatchlistItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = watchlist_service.add_to_watchlist(db, user_id=current_user.id, item_in=payload)
    return {
        "success": True,
        "message": "IPO added to watchlist successfully",
        "data": WatchlistItemResponse.model_validate(item)
    }

@router.put("/items/{item_id}", response_model=dict)
def update_watchlist_item(
    item_id: uuid.UUID,
    payload: WatchlistItemUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = watchlist_service.update_watchlist_item(
        db, user_id=current_user.id, item_id=item_id, update_in=payload
    )
    return {
        "success": True,
        "message": "Watchlist item updated successfully",
        "data": WatchlistItemResponse.model_validate(item)
    }

@router.delete("/{ipo_id}", response_model=dict)
def remove_from_watchlist(
    ipo_id: uuid.UUID,
    folder_id: Optional[uuid.UUID] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    watchlist_service.remove_from_watchlist(
        db, user_id=current_user.id, ipo_id=ipo_id, folder_id=folder_id
    )
    return {
        "success": True,
        "message": "IPO removed from watchlist successfully"
    }

@router.get("", response_model=dict)
def get_watchlist(
    folder_id: Optional[uuid.UUID] = Query(None),
    sort_by: str = Query("Newest"),
    ipo_status: Optional[str] = Query(None, alias="status"),
    sector: Optional[str] = Query(None),
    industry: Optional[str] = Query(None),
    ipo_type: Optional[str] = Query(None),
    recommendation: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    results, total = watchlist_service.list_watchlist(
        db,
        user_id=current_user.id,
        folder_id=folder_id,
        sort_by=sort_by,
        status_filter=ipo_status,
        sector_filter=sector,
        industry_filter=industry,
        ipo_type_filter=ipo_type,
        rec_filter=recommendation,
        limit=limit,
        offset=offset
    )
    return {
        "success": True,
        "message": "Watchlist retrieved successfully",
        "data": [WatchlistItemResponse.model_validate(item) for item in results],
        "meta": {
            "total": total,
            "limit": limit,
            "offset": offset
        }
    }

@router.get("/summary", response_model=dict)
def get_watchlist_summary(
    folder_id: Optional[uuid.UUID] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    summary = watchlist_service.get_summary(db, user_id=current_user.id, folder_id=folder_id)
    return {
        "success": True,
        "message": "Watchlist summary retrieved successfully",
        "data": summary
    }

@router.get("/count", response_model=dict)
def get_watchlist_count(
    folder_id: Optional[uuid.UUID] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    count = watchlist_service.get_count(db, user_id=current_user.id, folder_id=folder_id)
    return {
        "success": True,
        "message": "Watchlist count retrieved successfully",
        "data": {
            "count": count
        }
    }
