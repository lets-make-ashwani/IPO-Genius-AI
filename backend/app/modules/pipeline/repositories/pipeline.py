from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional, List, Tuple, Dict
import uuid
import datetime
from app.modules.pipeline.models.pipeline import (
    PipelineRun,
    PipelineRunItem,
    IPODocument,
    PipelineRunStatus,
    PipelineItemStatus,
)

class PipelineRunRepository:
    def create(self, db: Session, run: PipelineRun) -> PipelineRun:
        db.add(run)
        db.commit()
        db.refresh(run)
        return run

    def get_by_id(self, db: Session, run_id: uuid.UUID) -> Optional[PipelineRun]:
        return db.query(PipelineRun).filter(PipelineRun.id == run_id).first()

    def get_by_idempotency_key(self, db: Session, key: str) -> Optional[PipelineRun]:
        return db.query(PipelineRun).filter(PipelineRun.idempotency_key == key).first()

    def get_runs(self, db: Session, limit: int = 20, offset: int = 0) -> Tuple[List[PipelineRun], int]:
        query = db.query(PipelineRun)
        total = query.count()
        results = query.order_by(desc(PipelineRun.created_at)).offset(offset).limit(limit).all()
        return results, total

    def update(self, db: Session) -> None:
        db.commit()

pipeline_run_repository = PipelineRunRepository()

class PipelineRunItemRepository:
    def create(self, db: Session, item: PipelineRunItem) -> PipelineRunItem:
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    def get_by_id(self, db: Session, item_id: uuid.UUID) -> Optional[PipelineRunItem]:
        return db.query(PipelineRunItem).filter(PipelineRunItem.id == item_id).first()

    def get_items_for_run(
        self, db: Session, run_id: uuid.UUID, limit: int = 20, offset: int = 0
    ) -> Tuple[List[PipelineRunItem], int]:
        query = db.query(PipelineRunItem).filter(PipelineRunItem.run_id == run_id)
        total = query.count()
        results = query.order_by(PipelineRunItem.created_at).offset(offset).limit(limit).all()
        return results, total

    def get_by_source_identifier(self, db: Session, run_id: uuid.UUID, source_identifier: str) -> Optional[PipelineRunItem]:
        return (
            db.query(PipelineRunItem)
            .filter(PipelineRunItem.run_id == run_id, PipelineRunItem.source_identifier == source_identifier)
            .first()
        )

    def count_by_status(self, db: Session, run_id: uuid.UUID) -> Dict[str, int]:
        results = (
            db.query(PipelineRunItem.status, sa_func_count(PipelineRunItem.id))
            .filter(PipelineRunItem.run_id == run_id)
            .group_by(PipelineRunItem.status)
            .all()
        )
        return {status: count for status, count in results}

    def update(self, db: Session) -> None:
        db.commit()

# Helper for count
from sqlalchemy import func as sa_func
def sa_func_count(col):
    return sa_func.count(col)

pipeline_run_item_repository = PipelineRunItemRepository()

class IPODocumentRepository:
    def create(self, db: Session, doc: IPODocument) -> IPODocument:
        db.add(doc)
        db.commit()
        db.refresh(doc)
        return doc

    def get_by_ipo_id(self, db: Session, ipo_id: uuid.UUID) -> List[IPODocument]:
        return db.query(IPODocument).filter(IPODocument.ipo_id == ipo_id).all()

    def get_by_hash(self, db: Session, doc_hash: str) -> Optional[IPODocument]:
        return db.query(IPODocument).filter(IPODocument.document_hash == doc_hash).first()

ipo_document_repository = IPODocumentRepository()
