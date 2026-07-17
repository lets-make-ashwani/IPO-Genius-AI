from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
import uuid

from app.database.session import get_db
from app.modules.ai.schemas.analysis import (
    AIAnalysisResponse,
    AISummaryResponse,
    AIScoreResponse,
    AIRiskResponse,
)
from app.modules.ai.services.analysis import ai_analysis_service
from app.modules.ipos.services.ipo import ipo_service
from app.shared.exceptions import AppException

router = APIRouter(prefix="/ai", tags=["AI Analysis"])

@router.get("/analysis/{ipo_id_or_slug}", response_model=dict)
def get_ai_analysis(ipo_id_or_slug: str, db: Session = Depends(get_db)):
    analysis = ai_analysis_service.get_or_generate_analysis(db, ipo_id_or_slug)
    return {
        "success": True,
        "message": "AI analysis retrieved successfully",
        "data": AIAnalysisResponse.model_validate(analysis)
    }

@router.post("/analysis/{ipo_id}/regenerate", response_model=dict)
def regenerate_ai_analysis(ipo_id: uuid.UUID, db: Session = Depends(get_db)):
    ipo = ipo_service.get_ipo_by_id(db, ipo_id)
    if not ipo:
        raise AppException("IPO not found", status_code=status.HTTP_404_NOT_FOUND)
        
    analysis = ai_analysis_service.generate_analysis(db, ipo, async_generation=False)
    return {
        "success": True,
        "message": "AI analysis regenerated successfully",
        "data": AIAnalysisResponse.model_validate(analysis)
    }

@router.get("/summary/{ipo_id_or_slug}", response_model=dict)
def get_ai_summary(ipo_id_or_slug: str, db: Session = Depends(get_db)):
    analysis = ai_analysis_service.get_or_generate_analysis(db, ipo_id_or_slug)
    return {
        "success": True,
        "message": "AI summary retrieved successfully",
        "data": AISummaryResponse.model_validate(analysis)
    }

@router.get("/score/{ipo_id_or_slug}", response_model=dict)
def get_ai_score(ipo_id_or_slug: str, db: Session = Depends(get_db)):
    analysis = ai_analysis_service.get_or_generate_analysis(db, ipo_id_or_slug)
    return {
        "success": True,
        "message": "AI scores retrieved successfully",
        "data": AIScoreResponse.model_validate(analysis)
    }

@router.get("/risk/{ipo_id_or_slug}", response_model=dict)
def get_ai_risk(ipo_id_or_slug: str, db: Session = Depends(get_db)):
    analysis = ai_analysis_service.get_or_generate_analysis(db, ipo_id_or_slug)
    return {
        "success": True,
        "message": "AI risk analysis retrieved successfully",
        "data": AIRiskResponse.model_validate(analysis)
    }
