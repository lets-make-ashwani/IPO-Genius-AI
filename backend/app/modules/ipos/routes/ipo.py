from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional, List
import uuid

from app.database.session import get_db
from app.modules.ipos.models.ipo import IPOStatus, IPOType
from app.modules.ipos.schemas.ipo import IPOResponse, IPODetailExtendedResponse
from app.modules.ipos.services.ipo import ipo_service

router = APIRouter(prefix="/ipos", tags=["IPOs"])

@router.get("", response_model=dict)
def get_all_ipos(
    status_filter: Optional[IPOStatus] = Query(None, alias="status"),
    ipo_type: Optional[IPOType] = Query(None),
    search: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    results, total = ipo_service.get_ipos(
        db, ipo_status=status_filter, ipo_type=ipo_type, search=search, limit=limit, offset=offset
    )
    return {
        "success": True,
        "message": "IPOs retrieved successfully",
        "data": [IPOResponse.model_validate(ipo) for ipo in results],
        "meta": {
            "total": total,
            "limit": limit,
            "offset": offset
        }
    }

@router.get("/upcoming", response_model=dict)
def get_upcoming_ipos(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    results, total = ipo_service.get_ipos(
        db, ipo_status=IPOStatus.UPCOMING, limit=limit, offset=offset
    )
    return {
        "success": True,
        "message": "Upcoming IPOs retrieved successfully",
        "data": [IPOResponse.model_validate(ipo) for ipo in results],
        "meta": {
            "total": total,
            "limit": limit,
            "offset": offset
        }
    }

@router.get("/open", response_model=dict)
def get_open_ipos(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    results, total = ipo_service.get_ipos(
        db, ipo_status=IPOStatus.OPEN, limit=limit, offset=offset
    )
    return {
        "success": True,
        "message": "Open IPOs retrieved successfully",
        "data": [IPOResponse.model_validate(ipo) for ipo in results],
        "meta": {
            "total": total,
            "limit": limit,
            "offset": offset
        }
    }

@router.get("/closed", response_model=dict)
def get_closed_ipos(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    results, total = ipo_service.get_ipos(
        db, ipo_status=IPOStatus.CLOSED, limit=limit, offset=offset
    )
    return {
        "success": True,
        "message": "Closed IPOs retrieved successfully",
        "data": [IPOResponse.model_validate(ipo) for ipo in results],
        "meta": {
            "total": total,
            "limit": limit,
            "offset": offset
        }
    }

@router.get("/listed", response_model=dict)
def get_listed_ipos(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    results, total = ipo_service.get_ipos(
        db, ipo_status=IPOStatus.LISTED, limit=limit, offset=offset
    )
    return {
        "success": True,
        "message": "Listed IPOs retrieved successfully",
        "data": [IPOResponse.model_validate(ipo) for ipo in results],
        "meta": {
            "total": total,
            "limit": limit,
            "offset": offset
        }
    }

@router.get("/search", response_model=dict)
def search_ipos(
    q: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    results, total = ipo_service.get_ipos(
        db, search=q, limit=limit, offset=offset
    )
    return {
        "success": True,
        "message": f"Search results for query: {q}",
        "data": [IPOResponse.model_validate(ipo) for ipo in results],
        "meta": {
            "total": total,
            "limit": limit,
            "offset": offset
        }
    }

@router.get("/{id_or_slug}", response_model=dict)
def get_ipo_details(id_or_slug: str, db: Session = Depends(get_db)):
    try:
        ipo_id = uuid.UUID(id_or_slug)
        ipo = ipo_service.get_ipo_by_id(db, ipo_id)
    except ValueError:
        ipo = ipo_service.get_ipo_by_slug(db, id_or_slug)

    return {
        "success": True,
        "message": "IPO details retrieved successfully",
        "data": IPODetailExtendedResponse.model_validate(ipo)
    }
