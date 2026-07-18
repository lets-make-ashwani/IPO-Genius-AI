import uuid
import hashlib
import json
import logging
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from app.modules.pipeline.models.pipeline import (
    PipelineRun,
    PipelineRunItem,
    IPODocument,
    PipelineRunStatus,
    PipelineRunTrigger,
    PipelineItemStatus,
    PipelineItemStage,
)
from app.modules.pipeline.repositories.pipeline import (
    pipeline_run_repository,
    pipeline_run_item_repository,
    ipo_document_repository,
)
from app.modules.pipeline.services.providers import (
    get_ipo_data_provider,
    get_document_parser,
)
from app.modules.pipeline.services.storage import get_document_storage
from app.modules.pipeline.services.normalizer import Normalizer
from app.modules.pipeline.services.validator import IPODataValidator
from app.modules.ipos.models.ipo import IPO
from app.modules.ipos.models.detail import IPODetail
from app.modules.ipos.repositories.ipo import ipo_repository
from app.modules.ai.services.analysis import ai_analysis_service, AIAnalysisStatus
from app.modules.notifications.events.dispatcher import event_dispatcher
from app.shared.exceptions import AppException
from fastapi import status

logger = logging.getLogger("app")

class PipelineService:
    def __init__(self):
        self.normalizer = Normalizer()
        self.validator = IPODataValidator()

    def execute_pipeline_run(
        self,
        db: Session,
        provider_name: str,
        trigger: PipelineRunTrigger,
        admin_id: Optional[uuid.UUID] = None,
        idempotency_key: Optional[str] = None,
        force_reprocess: bool = False
    ) -> PipelineRun:
        """
        Main entry point for running the pipeline.
        Synchronous for Phase 9, but follows async status design.
        """
        # 1. Handle idempotency key
        if not idempotency_key:
            idempotency_key = f"run_{uuid.uuid4()}"

        existing_run = pipeline_run_repository.get_by_idempotency_key(db, idempotency_key)
        if existing_run:
            raise AppException("Pipeline run with this idempotency key already exists", status_code=status.HTTP_409_CONFLICT)

        # 2. Create the run record
        run = PipelineRun(
            id=uuid.uuid4(),
            idempotency_key=idempotency_key,
            status=PipelineRunStatus.RUNNING,
            trigger=trigger,
            source_provider=provider_name,
            triggered_by_admin_id=admin_id,
            started_at=datetime.now(timezone.utc),
            run_metadata={"force_reprocess": force_reprocess}
        )
        db.add(run)
        db.commit()
        db.refresh(run)

        try:
            self._run_core_logic(db, run, force_reprocess)
        except Exception as e:
            logger.error(f"Pipeline run level failure: {str(e)}", exc_info=True)
            run.status = PipelineRunStatus.FAILED
            run.error_message = str(e)
            run.completed_at = datetime.now(timezone.utc)
            db.commit()
            raise e

        return run

    def resume_pipeline_run(
        self,
        db: Session,
        run_id: uuid.UUID,
        force_reprocess: bool = False
    ) -> PipelineRun:
        """
        Resumes a partially completed run. Processes only items that are FAILED or PENDING.
        """
        run = pipeline_run_repository.get_by_id(db, run_id)
        if not run:
            raise AppException("Pipeline run not found", status_code=status.HTTP_404_NOT_FOUND)

        if run.status not in (PipelineRunStatus.PARTIAL, PipelineRunStatus.FAILED, PipelineRunStatus.PENDING):
            raise AppException(f"Cannot resume a pipeline run in status: {run.status}", status_code=status.HTTP_400_BAD_REQUEST)

        # Set to running
        run.status = PipelineRunStatus.RUNNING
        run.error_message = None
        run.started_at = datetime.now(timezone.utc)
        db.commit()

        try:
            self._run_core_logic(db, run, force_reprocess, resume=True)
        except Exception as e:
            logger.error(f"Pipeline run resume level failure: {str(e)}", exc_info=True)
            run.status = PipelineRunStatus.FAILED
            run.error_message = str(e)
            run.completed_at = datetime.now(timezone.utc)
            db.commit()
            raise e

        return run

    def _run_core_logic(self, db: Session, run: PipelineRun, force_reprocess: bool, resume: bool = False) -> None:
        provider = get_ipo_data_provider(run.source_provider)
        doc_parser = get_document_parser()
        doc_storage = get_document_storage()

        # 1. DISCOVERY
        raw_records = []
        if not resume:
            try:
                raw_records = provider.discover_ipos()
                run.total_discovered = len(raw_records)
                db.commit()
            except Exception as e:
                raise Exception(f"Failed to discover IPOs from provider {run.source_provider}: {str(e)}")

            # Create items in DB
            items = []
            for record in raw_records:
                # We compute hash of raw payload (excluding volatile/empty fields)
                source_data_hash = self._calculate_hash(record)
                
                # Exclude raw_source_data from permanent DB storage as requested to avoid bloated tables,
                # save only identifiers and structured summaries.
                item = PipelineRunItem(
                    id=uuid.uuid4(),
                    run_id=run.id,
                    source_identifier=record["source_identifier"],
                    company_name=record["company_name"],
                    status=PipelineItemStatus.PENDING,
                    current_stage=PipelineItemStage.DISCOVERY,
                    source_data_hash=source_data_hash,
                    extracted_data=record # Storing original record fields (lightweight)
                )
                db.add(item)
                items.append(item)
            db.commit()
        else:
            # Resuming - retrieve failed or pending items
            items = db.query(PipelineRunItem).filter(
                PipelineRunItem.run_id == run.id,
                PipelineRunItem.status.in_([PipelineItemStatus.FAILED, PipelineItemStatus.PENDING])
            ).all()

        # 2. Sequential processing of each item
        for item in items:
            item.status = PipelineItemStatus.RUNNING
            item.started_at = datetime.now(timezone.utc)
            item.error_message = None
            db.commit()

            try:
                self._process_single_item(db, run, item, doc_parser, doc_storage, force_reprocess)
            except Exception as e:
                logger.error(f"Failed to process pipeline item {item.company_name}: {str(e)}")
                item.status = PipelineItemStatus.FAILED
                item.error_message = str(e)
                item.completed_at = datetime.now(timezone.utc)
                db.commit()

        # 3. Finalize run counters and status
        self._finalize_run_status(db, run)

    def _process_single_item(
        self,
        db: Session,
        run: PipelineRun,
        item: PipelineRunItem,
        doc_parser,
        doc_storage,
        force_reprocess: bool
    ) -> None:
        # Resolve existing IPO by provider + identifier, fallback to slug/company name to prevent duplicates
        ipo = self._find_existing_ipo(db, run.source_provider, item.source_identifier, item.company_name)

        # Idempotency Check: if unchanged and not forced
        if ipo and ipo.source_data_hash == item.source_data_hash and not force_reprocess:
            item.status = PipelineItemStatus.SKIPPED
            item.current_stage = PipelineItemStage.COMPLETED
            item.ipo_id = ipo.id
            item.completed_at = datetime.now(timezone.utc)
            db.commit()
            return

        record = item.extracted_data or {}

        # Stage: DOCUMENT FETCH & PARSE
        if item.current_stage == PipelineItemStage.DISCOVERY or item.current_stage == PipelineItemStage.DOCUMENT_FETCH:
            item.current_stage = PipelineItemStage.DOCUMENT_FETCH
            db.commit()
            
            # Fetch and parse DRHP / RHP documents if urls are available
            urls_to_fetch = {
                "DRHP": record.get("drhp_url"),
                "RHP": record.get("rhp_url"),
                "PROSPECTUS": record.get("prospectus_url"),
            }
            parsed_docs = {}
            for doc_type, url in urls_to_fetch.items():
                if url:
                    # Parse document (mock or real)
                    parsed_doc = doc_parser.parse_document(url, doc_type)
                    parsed_docs[doc_type] = parsed_doc
            
            # Store in item.extracted_data (merged result)
            record["_parsed_documents"] = parsed_docs
            item.extracted_data = record
            item.current_stage = PipelineItemStage.EXTRACTION
            db.commit()

        # Stage: EXTRACTION & MERGING
        if item.current_stage == PipelineItemStage.EXTRACTION:
            # We merge parsed fields if available
            parsed_docs = record.get("_parsed_documents", {})
            for doc_type, p_content in parsed_docs.items():
                ext_fields = p_content.get("extracted_fields", {})
                # E.g. fill details if not provided by source feed
                if ext_fields:
                    if not record.get("company_overview") and ext_fields.get("company_overview"):
                        record["company_overview"] = ext_fields["company_overview"]
                    if not record.get("business_model") and ext_fields.get("business_model"):
                        record["business_model"] = ext_fields["business_model"]
                    if not record.get("promoters") and ext_fields.get("promoters"):
                        record["promoters"] = ext_fields["promoters"]
                    if not record.get("objectives") and ext_fields.get("objectives"):
                        record["objectives"] = ext_fields["objectives"]
                    if not record.get("financial_summary") and ext_fields.get("financial_summary"):
                        record["financial_summary"] = ext_fields["financial_summary"]
            
            item.extracted_data = record
            item.current_stage = PipelineItemStage.NORMALIZATION
            db.commit()

        # Stage: NORMALIZATION (Dedicated layer)
        if item.current_stage == PipelineItemStage.NORMALIZATION:
            normalized_record = self.normalizer.normalize(record)
            item.normalized_data = normalized_record
            item.current_stage = PipelineItemStage.VALIDATION
            db.commit()

        # Stage: VALIDATION
        if item.current_stage == PipelineItemStage.VALIDATION:
            norm_rec = item.normalized_data
            val_res = self.validator.validate(norm_rec)
            item.validation_errors = {
                "errors": val_res["errors"],
                "warnings": val_res["warnings"]
            }
            if not val_res["is_valid"]:
                raise Exception(f"Validation failed: {', '.join(val_res['errors'])}")
            
            item.current_stage = PipelineItemStage.IPO_UPSERT
            db.commit()

        norm_rec = item.normalized_data

        # Stage: IPO UPSERT
        if item.current_stage == PipelineItemStage.IPO_UPSERT:
            is_new_ipo = False
            if not ipo:
                is_new_ipo = True
                # Generate slug
                slug = self._generate_slug(db, norm_rec["company_name"])
                ipo = IPO(
                    id=uuid.uuid4(),
                    company_name=norm_rec["company_name"],
                    slug=slug,
                    logo_url=norm_rec["logo_url"],
                    sector=norm_rec["sector"],
                    industry=norm_rec["industry"],
                    exchange=norm_rec["exchange"],
                    ipo_type=norm_rec["ipo_type"],
                    price_band=norm_rec["price_band"],
                    lot_size=norm_rec["lot_size"],
                    issue_size=norm_rec["issue_size"],
                    open_date=norm_rec["open_date"],
                    close_date=norm_rec["close_date"],
                    listing_date=norm_rec["listing_date"],
                    status=norm_rec["status"],
                    gmp=norm_rec["gmp"],
                    drhp_url=norm_rec["drhp_url"],
                    rhp_url=norm_rec["rhp_url"],
                    prospectus_url=norm_rec["prospectus_url"],
                    source=run.source_provider,
                    source_url=norm_rec["source_url"],
                    source_identifier=item.source_identifier,
                    source_data_hash=item.source_data_hash,
                    is_verified=True,
                    last_synced_at=datetime.now(timezone.utc)
                )
                
                # IPO Details
                details = IPODetail(
                    id=uuid.uuid4(),
                    ipo_id=ipo.id,
                    company_overview=norm_rec["company_overview"],
                    business_model=norm_rec["business_model"],
                    promoters=norm_rec["promoters"],
                    objectives=norm_rec["objectives"],
                    financial_summary=norm_rec["financial_summary"]
                )
                ipo.details = details
                db.add(ipo)
            else:
                # Update existing
                ipo.company_name = norm_rec["company_name"]
                ipo.logo_url = norm_rec["logo_url"]
                ipo.sector = norm_rec["sector"]
                ipo.industry = norm_rec["industry"]
                ipo.exchange = norm_rec["exchange"]
                ipo.ipo_type = norm_rec["ipo_type"]
                ipo.price_band = norm_rec["price_band"]
                ipo.lot_size = norm_rec["lot_size"]
                ipo.issue_size = norm_rec["issue_size"]
                ipo.open_date = norm_rec["open_date"]
                ipo.close_date = norm_rec["close_date"]
                ipo.listing_date = norm_rec["listing_date"]
                ipo.status = norm_rec["status"]
                ipo.gmp = norm_rec["gmp"]
                ipo.drhp_url = norm_rec["drhp_url"]
                ipo.rhp_url = norm_rec["rhp_url"]
                ipo.prospectus_url = norm_rec["prospectus_url"]
                ipo.source = run.source_provider
                ipo.source_url = norm_rec["source_url"]
                ipo.source_identifier = item.source_identifier
                ipo.source_data_hash = item.source_data_hash
                ipo.last_synced_at = datetime.now(timezone.utc)
                ipo.is_verified = True

                if not ipo.details:
                    ipo.details = IPODetail(id=uuid.uuid4(), ipo_id=ipo.id)
                ipo.details.company_overview = norm_rec["company_overview"]
                ipo.details.business_model = norm_rec["business_model"]
                ipo.details.promoters = norm_rec["promoters"]
                ipo.details.objectives = norm_rec["objectives"]
                ipo.details.financial_summary = norm_rec["financial_summary"]

            db.commit()
            db.refresh(ipo)
            
            # Create IPODocument records in db for version audit tracking
            parsed_docs = record.get("_parsed_documents", {})
            for doc_type, p_content in parsed_docs.items():
                # Check if this document already exists to avoid duplication
                existing_doc = db.query(IPODocument).filter(
                    IPODocument.ipo_id == ipo.id,
                    IPODocument.document_hash == p_content["document_hash"]
                ).first()
                if not existing_doc:
                    # Write dummy file to storage as placeholder for LocalDocumentStorage skeleton
                    dummy_bytes = p_content["raw_text"].encode("utf-8")
                    file_name = f"{ipo.slug}_{doc_type.lower()}_v{p_content['document_version']}.pdf"
                    saved_path = doc_storage.save(file_name, dummy_bytes)

                    db_doc = IPODocument(
                        id=uuid.uuid4(),
                        ipo_id=ipo.id,
                        document_type=doc_type,
                        file_path=saved_path,
                        document_version=p_content["document_version"],
                        document_hash=p_content["document_hash"],
                        document_size=p_content["document_size"],
                        mime_type=p_content["mime_type"]
                    )
                    db.add(db_doc)
            db.commit()

            item.ipo_id = ipo.id
            item.current_stage = PipelineItemStage.AI_GENERATION
            db.commit()

        # Stage: AI GENERATION
        if item.current_stage == PipelineItemStage.AI_GENERATION:
            # Check settings
            from app.config.settings import settings
            if settings.PIPELINE_AI_AUTO_TRIGGER:
                logger.info(f"Auto-triggering AI Analysis for IPO: {ipo.company_name}")
                # We call generate_analysis directly to force run since data is updated or brand new
                analysis = ai_analysis_service.generate_analysis(db, ipo, async_generation=False)
                
                # Capture metrics
                item.ai_provider = analysis.provider or "MOCK"
                item.ai_model = analysis.model_name or "mock-llm-v1"
                item.ai_tokens_used = analysis.tokens_used or 0
                item.ai_processing_time_ms = analysis.processing_time_ms or 0
                # Calculate estimated cost
                item.ai_estimated_cost = (item.ai_tokens_used / 1000.0) * 0.015
                
            item.current_stage = PipelineItemStage.NOTIFICATION
            db.commit()

        # Stage: NOTIFICATION
        if item.current_stage == PipelineItemStage.NOTIFICATION:
            # We trigger the dispatcher events
            # New IPO or Status Update
            is_new = (item.retry_count == 0 and not force_reprocess) # simple approximation
            event_dispatcher.dispatch("IPO_STATUS_UPDATE", db=db, ipo=ipo)
            
            # AI generation completed
            event_dispatcher.dispatch("AI_ANALYSIS_COMPLETED", db=db, ipo=ipo)
            
            item.status = PipelineItemStatus.COMPLETED
            item.current_stage = PipelineItemStage.COMPLETED
            item.completed_at = datetime.now(timezone.utc)
            db.commit()

    def _find_existing_ipo(self, db: Session, provider: str, source_identifier: str, company_name: str) -> Optional[IPO]:
        # 1. Match by provider + source_identifier
        ipo = db.query(IPO).filter(
            IPO.source == provider,
            IPO.source_identifier == source_identifier
        ).first()
        if ipo:
            return ipo

        # 2. Fallback: match by unique company name
        ipo = db.query(IPO).filter(IPO.company_name == company_name).first()
        if ipo:
            return ipo

        # 3. Fallback: match by slug
        import re
        base_slug = company_name.lower()
        base_slug = re.sub(r'[^a-z0-9\s-]', '', base_slug)
        base_slug = re.sub(r'[\s-]+', '-', base_slug)
        base_slug = base_slug.strip('-')
        
        ipo = db.query(IPO).filter(IPO.slug == base_slug).first()
        return ipo

    def _generate_slug(self, db: Session, company_name: str) -> str:
        import re
        base_slug = company_name.lower()
        base_slug = re.sub(r'[^a-z0-9\s-]', '', base_slug)
        base_slug = re.sub(r'[\s-]+', '-', base_slug)
        base_slug = base_slug.strip('-')
        
        slug = base_slug
        counter = 1
        while db.query(IPO).filter(IPO.slug == slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    def _calculate_hash(self, record: Dict[str, Any]) -> str:
        # Compute SHA256 of stable values
        hasher = hashlib.sha256()
        stable_keys = ["company_name", "price_band", "lot_size", "issue_size", "open_date", "close_date"]
        values = []
        for k in stable_keys:
            values.append(str(record.get(k, "")))
        content = "||".join(values)
        hasher.update(content.encode("utf-8"))
        return hasher.hexdigest()

    def _finalize_run_status(self, db: Session, run: PipelineRun) -> None:
        counts = pipeline_run_item_repository.count_by_status(db, run.id)
        
        total_completed = counts.get(PipelineItemStatus.COMPLETED, 0)
        total_skipped = counts.get(PipelineItemStatus.SKIPPED, 0)
        total_failed = counts.get(PipelineItemStatus.FAILED, 0)

        run.total_processed = total_completed
        run.total_skipped = total_skipped
        run.total_failed = total_failed

        if total_failed > 0:
            if total_completed > 0 or total_skipped > 0:
                run.status = PipelineRunStatus.PARTIAL
            else:
                run.status = PipelineRunStatus.FAILED
        else:
            run.status = PipelineRunStatus.COMPLETED

        run.completed_at = datetime.now(timezone.utc)
        db.commit()

pipeline_service = PipelineService()
