from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
import uuid
from typing import Optional, List, Dict, Any

from app.database.session import get_db
from app.shared.dependencies import get_current_user, RoleChecker
from app.modules.users.models import User
from app.modules.admin.services.admin import admin_service
from app.modules.admin.schemas.admin import (
    AdminDashboardResponse,
    AdminUserResponse,
    AdminUserUpdatePayload,
    DashboardData,
    ActivityLogEntry,
    SignupStats
)
from app.modules.ipos.schemas.ipo import IPOCreate, IPOUpdate, IPODetailExtendedResponse
from app.modules.ipos.services.ipo import ipo_service
from app.modules.ai.schemas.analysis import AIAnalysisResponse
from app.modules.users.repositories.activity import user_activity_repository

router = APIRouter(prefix="/admin", tags=["Admin Panel"])
require_admin = Depends(RoleChecker(["ADMIN"]))

@router.get("/dashboard", response_model=AdminDashboardResponse)
def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    _role_check = require_admin
):
    data = admin_service.get_dashboard_analytics(db)
    return {
        "success": True,
        "message": "Dashboard analytics retrieved successfully",
        "data": DashboardData(
            total_users=data["total_users"],
            total_ipos=data["total_ipos"],
            total_watchlist_items=data["total_watchlist_items"],
            total_ai_analyses=data["total_ai_analyses"],
            recent_signups=[SignupStats(**x) for x in data["recent_signups"]],
            recent_activities=[
                ActivityLogEntry(
                    id=act.id,
                    user_id=act.user_id,
                    action=act.action,
                    metadata_json=act.metadata_json,
                    created_at=act.created_at
                )
                for act in data["recent_activities"]
            ]
        )
    }

@router.get("/users", response_model=Dict[str, Any])
def list_users(
    search: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    _role_check = require_admin
):
    results, total = admin_service.list_users(
        db, search=search, role=role, is_active=is_active, limit=limit, offset=offset
    )
    return {
        "success": True,
        "message": "Users list retrieved successfully",
        "data": [AdminUserResponse.model_validate(u) for u in results],
        "meta": {
            "total": total,
            "limit": limit,
            "offset": offset
        }
    }

@router.put("/users/{user_id}", response_model=Dict[str, Any])
def update_user(
    user_id: uuid.UUID,
    payload: AdminUserUpdatePayload,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    _role_check = require_admin
):
    updated = admin_service.update_user(
        db, admin_user_id=current_user.id, target_user_id=user_id, payload=payload
    )
    return {
        "success": True,
        "message": "User updated successfully",
        "data": AdminUserResponse.model_validate(updated)
    }

@router.delete("/users/{user_id}", response_model=Dict[str, Any])
def deactivate_user(
    user_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    _role_check = require_admin
):
    deactivated = admin_service.deactivate_user_account(
        db, admin_user_id=current_user.id, target_user_id=user_id
    )
    return {
        "success": True,
        "message": "User account deactivated successfully",
        "data": AdminUserResponse.model_validate(deactivated)
    }

@router.get("/ipos", response_model=Dict[str, Any])
def list_ipos(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    _role_check = require_admin
):
    results, total = ipo_service.get_ipos(db, limit=limit, offset=offset)
    return {
        "success": True,
        "message": "IPOs retrieved successfully",
        "data": [IPODetailExtendedResponse.model_validate(i) for i in results],
        "meta": {
            "total": total,
            "limit": limit,
            "offset": offset
        }
    }

@router.post("/ipos", response_model=Dict[str, Any])
def create_ipo(
    payload: IPOCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    _role_check = require_admin
):
    ipo = ipo_service.create_ipo(db, payload)
    
    # Log audit
    user_activity_repository.log_activity(
        db,
        user_id=current_user.id,
        action="ADMIN_IPO_CREATED",
        metadata_json={"ipo_id": str(ipo.id), "company_name": ipo.company_name}
    )
    
    return {
        "success": True,
        "message": "IPO created successfully",
        "data": IPODetailExtendedResponse.model_validate(ipo)
    }

@router.put("/ipos/{ipo_id}", response_model=Dict[str, Any])
def update_ipo(
    ipo_id: uuid.UUID,
    payload: IPOUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    _role_check = require_admin
):
    ipo = ipo_service.update_ipo(db, ipo_id=ipo_id, ipo_data=payload)
    
    # Log audit
    user_activity_repository.log_activity(
        db,
        user_id=current_user.id,
        action="ADMIN_IPO_UPDATED",
        metadata_json={"ipo_id": str(ipo.id), "company_name": ipo.company_name}
    )
    
    return {
        "success": True,
        "message": "IPO updated successfully",
        "data": IPODetailExtendedResponse.model_validate(ipo)
    }

@router.delete("/ipos/{ipo_id}", response_model=Dict[str, Any])
def delete_ipo(
    ipo_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    _role_check = require_admin
):
    # Fetch details first for logging metadata
    ipo = ipo_service.get_ipo_by_id(db, ipo_id)
    company_name = ipo.company_name
    
    ipo_service.delete_ipo(db, ipo_id=ipo_id)
    
    # Log audit
    user_activity_repository.log_activity(
        db,
        user_id=current_user.id,
        action="ADMIN_IPO_DELETED",
        metadata_json={"ipo_id": str(ipo_id), "company_name": company_name}
    )
    
    return {
        "success": True,
        "message": "IPO deleted successfully"
    }

@router.post("/ai/run/{ipo_id}", response_model=Dict[str, Any])
def trigger_ai_run(
    ipo_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    _role_check = require_admin
):
    analysis = admin_service.trigger_ai_analysis(db, admin_user_id=current_user.id, ipo_id=ipo_id)
    return {
        "success": True,
        "message": "AI analysis triggered successfully",
        "data": AIAnalysisResponse.model_validate(analysis)
    }
