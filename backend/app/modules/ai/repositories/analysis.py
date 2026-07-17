from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import Optional, List
import uuid
from app.modules.ai.models.analysis import AIAnalysis

class AIAnalysisRepository:
    def get_active_by_ipo_id(self, db: Session, ipo_id: uuid.UUID) -> Optional[AIAnalysis]:
        return (
            db.query(AIAnalysis)
            .filter(AIAnalysis.ipo_id == ipo_id, AIAnalysis.is_active == True)
            .first()
        )

    def get_history_by_ipo_id(self, db: Session, ipo_id: uuid.UUID) -> List[AIAnalysis]:
        return (
            db.query(AIAnalysis)
            .filter(AIAnalysis.ipo_id == ipo_id)
            .order_by(desc(AIAnalysis.version))
            .all()
        )

    def get_max_version_for_ipo(self, db: Session, ipo_id: uuid.UUID) -> int:
        max_v = db.query(func.max(AIAnalysis.version)).filter(AIAnalysis.ipo_id == ipo_id).scalar()
        return max_v if max_v is not None else 0

    def deactivate_all_for_ipo(self, db: Session, ipo_id: uuid.UUID) -> None:
        db.query(AIAnalysis).filter(AIAnalysis.ipo_id == ipo_id).update({"is_active": False})
        db.commit()

    def create(self, db: Session, obj: AIAnalysis) -> AIAnalysis:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

ai_analysis_repository = AIAnalysisRepository()
