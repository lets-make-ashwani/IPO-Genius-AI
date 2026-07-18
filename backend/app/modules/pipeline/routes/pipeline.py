from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
import uuid

from app.database.session import get_db
from app.modules.users.models import User
from app.shared.dependencies import RoleChecker, get_current_user
from app.modules.users.repositories.activity import user_activity_repository
from app.modules.pipeline.services.pipeline import pipeline_service
from app.modules.pipeline.repositories.pipeline import (
    pipeline_run_repository,
    pipeline_run_item_repository,
)
from app.modules.pipeline.schemas.pipeline import (
    PipelineTriggerRequest,
    PipelineRunSummaryResponse,
    PipelineRunResponse,
    PipelineRunItemResponse,
    PipelineRunListResponse,
)
from app.modules.pipeline.models.pipeline import PipelineRunTrigger, PipelineRunStatus

router = APIRouter(prefix="/admin/pipeline", tags=["Admin – Pipeline"])

# Protect all routes to only be accessible by ADMIN
admin_checker = RoleChecker(["ADMIN"])

@router.post("/run", response_model=PipelineRunSummaryResponse, status_code=status.HTTP_200_OK)
def trigger_pipeline_run(
    payload: PipelineTriggerRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_checker),
):
    """
    Trigger a new pipeline run.
    This runs synchronously for Phase 9, but simulates async statuses.
    """
    run = pipeline_service.execute_pipeline_run(
        db=db,
        provider_name=payload.provider,
        trigger=PipelineRunTrigger.MANUAL,
        admin_id=current_user.id,
        idempotency_key=payload.idempotency_key,
        force_reprocess=payload.force_reprocess,
    )

    # Log admin audit log
    user_activity_repository.log_activity(
        db=db,
        user_id=current_user.id,
        action="ADMIN_PIPELINE_RUN_TRIGGERED",
        metadata_json={
            "run_id": str(run.id),
            "provider": payload.provider,
            "idempotency_key": run.idempotency_key,
            "force_reprocess": payload.force_reprocess,
        }
    )

    return run

@router.post("/runs/{run_id}/resume", response_model=PipelineRunSummaryResponse, status_code=status.HTTP_200_OK)
def resume_pipeline_run(
    run_id: uuid.UUID,
    force_reprocess: bool = Query(False),
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_checker),
):
    """
    Resume a partially failed, pending, or run-level failed pipeline run.
    Processes only the items that did not succeed previously.
    """
    run = pipeline_service.resume_pipeline_run(
        db=db,
        run_id=run_id,
        force_reprocess=force_reprocess,
    )

    # Log admin audit log
    user_activity_repository.log_activity(
        db=db,
        user_id=current_user.id,
        action="ADMIN_PIPELINE_RUN_RESUMED",
        metadata_json={
            "run_id": str(run.id),
            "force_reprocess": force_reprocess,
        }
    )

    return run

@router.get("/runs", response_model=PipelineRunListResponse)
def list_pipeline_runs(
    status_filter: Optional[PipelineRunStatus] = Query(None, alias="status"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_checker),
):
    """
    Get paginated history of all pipeline runs.
    """
    # Just query PipelineRun
    from app.modules.pipeline.models.pipeline import PipelineRun
    query = db.query(PipelineRun)
    if status_filter:
        query = query.filter(PipelineRun.status == status_filter.value)
    
    total = query.count()
    items = query.order_by(PipelineRun.created_at.desc()).offset(offset).limit(limit).all()

    return PipelineRunListResponse(
        items=items,
        total=total,
        limit=limit,
        offset=offset
    )

@router.get("/runs/{run_id}", response_model=PipelineRunResponse)
def get_pipeline_run(
    run_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_checker),
):
    """
    Get detailed metrics of a specific pipeline run, including its list of run items.
    """
    run = pipeline_run_repository.get_by_id(db, run_id)
    if not run:
        from app.shared.exceptions import AppException
        raise AppException("Pipeline run not found", status_code=status.HTTP_404_NOT_FOUND)
    
    # Use simpler query
    from app.modules.pipeline.models.pipeline import PipelineRunItem
    items = db.query(PipelineRunItem).filter(PipelineRunItem.run_id == run_id).all()
    
    # Construct response
    resp = PipelineRunResponse.model_validate(run)
    resp.items = [PipelineRunItemResponse.model_validate(i) for i in items]
    return resp

@router.get("/runs/{run_id}/items", response_model=List[PipelineRunItemResponse])
def get_pipeline_run_items(
    run_id: uuid.UUID,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_checker),
):
    """
    Get items for a specific run with pagination.
    """
    items, total = pipeline_run_item_repository.get_items_for_run(db, run_id, limit, offset)
    return items

@router.get("/runs/{run_id}/items/{item_id}", response_model=PipelineRunItemResponse)
def get_pipeline_run_item_detail(
    run_id: uuid.UUID,
    item_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_checker),
):
    """
    Get a single pipeline item details (useful for checking extracted fields, normalization, validation errors).
    """
    item = pipeline_run_item_repository.get_by_id(db, item_id)
    if not item or item.run_id != run_id:
        from app.shared.exceptions import AppException
        raise AppException("Pipeline item not found", status_code=status.HTTP_404_NOT_FOUND)
    return item
