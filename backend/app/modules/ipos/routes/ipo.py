from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional, List
import uuid

from app.database.session import get_db
from app.modules.ipos.models.ipo import IPOStatus, IPOType
from app.modules.ipos.schemas.ipo import (
    IPOResponse,
    IPODetailExtendedResponse,
    IPOAnalysisResponse,
    IPOFinancialsResponse,
    IPOSubscriptionResponse,
    IPODocumentsResponse,
    IPONewsResponse,
)
from app.modules.ipos.services.ipo import ipo_service

router = APIRouter(prefix="/ipos", tags=["IPOs"])

def _format_paginated_response(message: str, items: list, total: any, limit: int, offset: int):
    try:
        total_count = int(total)
    except (TypeError, ValueError):
        total_count = len(items)

    return {
        "success": True,
        "message": message,
        "data": [IPOResponse.model_validate(ipo) for ipo in items],
        "pagination": {
            "total": total_count,
            "limit": limit,
            "offset": offset,
            "has_next": (offset + limit) < total_count,
            "has_prev": offset > 0
        },
        "meta": {
            "total": total_count,
            "limit": limit,
            "offset": offset
        }
    }

@router.get("", response_model=dict)
def get_all_ipos(
    status_filter: Optional[IPOStatus] = Query(None, alias="status"),
    ipo_type: Optional[IPOType] = Query(None),
    exchange: Optional[str] = Query(None),
    sector: Optional[str] = Query(None),
    industry: Optional[str] = Query(None),
    search: Optional[str] = Query(None, alias="search"),
    sort_by: Optional[str] = Query("open_date"),
    sort_order: Optional[str] = Query("desc"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    results, total = ipo_service.get_ipos(
        db,
        ipo_status=status_filter,
        ipo_type=ipo_type,
        exchange=exchange,
        sector=sector,
        industry=industry,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        limit=limit,
        offset=offset
    )
    return _format_paginated_response("IPOs retrieved successfully", results, total, limit, offset)

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
    return _format_paginated_response(f"Search results for query: {q}", results, total, limit, offset)

@router.get("/upcoming", response_model=dict)
def get_upcoming_ipos(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    results, total = ipo_service.get_ipos(
        db, ipo_status=IPOStatus.UPCOMING, limit=limit, offset=offset
    )
    return _format_paginated_response("Upcoming IPOs retrieved successfully", results, total, limit, offset)

@router.get("/open", response_model=dict)
def get_open_ipos(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    results, total = ipo_service.get_ipos(
        db, ipo_status=IPOStatus.OPEN, limit=limit, offset=offset
    )
    return _format_paginated_response("Open IPOs retrieved successfully", results, total, limit, offset)

@router.get("/listed", response_model=dict)
def get_listed_ipos(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    results, total = ipo_service.get_ipos(
        db, ipo_status=IPOStatus.LISTED, limit=limit, offset=offset
    )
    return _format_paginated_response("Listed IPOs retrieved successfully", results, total, limit, offset)

@router.get("/closed", response_model=dict)
def get_closed_ipos(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    results, total = ipo_service.get_ipos(
        db, ipo_status=IPOStatus.CLOSED, limit=limit, offset=offset
    )
    return _format_paginated_response("Closed IPOs retrieved successfully", results, total, limit, offset)


# --- Phase 3.2: Sub-resource Endpoints ---

@router.get("/{id_or_slug}/analysis", response_model=dict)
def get_ipo_analysis(id_or_slug: str, db: Session = Depends(get_db)):
    try:
        ipo_id = uuid.UUID(id_or_slug)
        ipo = ipo_service.get_ipo_by_id(db, ipo_id)
    except ValueError:
        ipo = ipo_service.get_ipo_by_slug(db, id_or_slug)

    analysis_data = ipo_service.get_ipo_analysis(db, ipo.id)
    return {
        "success": True,
        "message": "AI Analysis retrieved successfully",
        "data": IPOAnalysisResponse.model_validate(analysis_data)
    }

@router.get("/{id_or_slug}/financials", response_model=dict)
def get_ipo_financials(id_or_slug: str, db: Session = Depends(get_db)):
    try:
        ipo_id = uuid.UUID(id_or_slug)
        ipo = ipo_service.get_ipo_by_id(db, ipo_id)
    except ValueError:
        ipo = ipo_service.get_ipo_by_slug(db, id_or_slug)

    fin_data = ipo_service.get_ipo_financials(db, ipo.id)
    return {
        "success": True,
        "message": "IPO Financials retrieved successfully",
        "data": IPOFinancialsResponse.model_validate(fin_data)
    }

@router.get("/{id_or_slug}/subscription", response_model=dict)
def get_ipo_subscription(id_or_slug: str, db: Session = Depends(get_db)):
    try:
        ipo_id = uuid.UUID(id_or_slug)
        ipo = ipo_service.get_ipo_by_id(db, ipo_id)
    except ValueError:
        ipo = ipo_service.get_ipo_by_slug(db, id_or_slug)

    sub_data = ipo_service.get_ipo_subscription(db, ipo.id)
    return {
        "success": True,
        "message": "IPO Subscriptions retrieved successfully",
        "data": IPOSubscriptionResponse.model_validate(sub_data)
    }

@router.get("/{id_or_slug}/documents", response_model=dict)
def get_ipo_documents(id_or_slug: str, db: Session = Depends(get_db)):
    try:
        ipo_id = uuid.UUID(id_or_slug)
        ipo = ipo_service.get_ipo_by_id(db, ipo_id)
    except ValueError:
        ipo = ipo_service.get_ipo_by_slug(db, id_or_slug)

    doc_data = ipo_service.get_ipo_documents(db, ipo.id)
    return {
        "success": True,
        "message": "IPO Regulatory Documents retrieved successfully",
        "data": IPODocumentsResponse.model_validate(doc_data)
    }

@router.get("/{id_or_slug}/news", response_model=dict)
def get_ipo_news(id_or_slug: str, db: Session = Depends(get_db)):
    try:
        ipo_id = uuid.UUID(id_or_slug)
        ipo = ipo_service.get_ipo_by_id(db, ipo_id)
    except ValueError:
        ipo = ipo_service.get_ipo_by_slug(db, id_or_slug)

    news_data = ipo_service.get_ipo_news(db, ipo.id)
    return {
        "success": True,
        "message": "IPO Related News retrieved successfully",
        "data": IPONewsResponse.model_validate(news_data)
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

