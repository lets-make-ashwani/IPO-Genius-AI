from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Tuple
import uuid
import hashlib
import logging

from app.modules.ai.models.analysis import AIAnalysis, AIAnalysisStatus, AIRecommendation
from app.modules.ai.repositories.analysis import ai_analysis_repository
from app.modules.ai.services.provider import BaseAIProvider, MockAIProvider
from app.modules.ipos.services.ipo import ipo_service
from app.shared.exceptions import AppException
from fastapi import status

logger = logging.getLogger("app")

class AIAnalysisService:
    def __init__(self, provider: BaseAIProvider = MockAIProvider()):
        self.provider = provider

    def calculate_ipo_hash(self, ipo) -> str:
        hasher = hashlib.sha256()
        fields = [
            ipo.company_name or "",
            ipo.price_band or "",
            ipo.issue_size or "",
            str(ipo.open_date or ""),
            str(ipo.close_date or ""),
        ]
        if ipo.details:
            fields.extend([
                ipo.details.company_overview or "",
                ipo.details.business_model or "",
                ipo.details.promoters or "",
                ipo.details.objectives or "",
                ipo.details.financial_summary or "",
            ])
        content = "||".join(fields)
        hasher.update(content.encode("utf-8"))
        return hasher.hexdigest()

    def get_or_generate_analysis(self, db: Session, ipo_id_or_slug: str) -> AIAnalysis:
        # 1. Resolve IPO
        try:
            ipo_uuid = uuid.UUID(ipo_id_or_slug)
            ipo = ipo_service.get_ipo_by_id(db, ipo_uuid)
        except ValueError:
            ipo = ipo_service.get_ipo_by_slug(db, ipo_id_or_slug)

        if not ipo:
            raise AppException("IPO not found", status_code=status.HTTP_404_NOT_FOUND)

        # 2. Get active analysis
        analysis = ai_analysis_repository.get_active_by_ipo_id(db, ipo.id)
        current_hash = self.calculate_ipo_hash(ipo)

        # 3. Check cache validity
        if analysis:
            is_hash_matching = (analysis.source_hash == current_hash)
            is_cache_valid = (analysis.cache_expires_at is None or analysis.cache_expires_at > datetime.now(timezone.utc))
            
            if is_hash_matching and is_cache_valid and analysis.status == AIAnalysisStatus.COMPLETED:
                # Mark as loaded from cache
                analysis.is_cached = True
                db.commit()
                return analysis

        # 4. Trigger generation (missing or stale/dirty cache)
        logger.info(f"Triggering AI Analysis generation for IPO: {ipo.company_name}")
        return self.generate_analysis(db, ipo, async_generation=False)

    def generate_analysis(self, db: Session, ipo, async_generation: bool = False) -> AIAnalysis:
        # Calculate source hash
        source_hash = self.calculate_ipo_hash(ipo)

        # Deactivate previous active versions
        ai_analysis_repository.deactivate_all_for_ipo(db, ipo.id)
        max_v = ai_analysis_repository.get_max_version_for_ipo(db, ipo.id)

        # Create new analysis in status PROCESSING or COMPLETED
        analysis = AIAnalysis(
            id=uuid.uuid4(),
            ipo_id=ipo.id,
            is_active=True,
            version=max_v + 1,
            status=AIAnalysisStatus.PROCESSING if async_generation else AIAnalysisStatus.COMPLETED,
            source_hash=source_hash,
            is_cached=False,
            generated_at=datetime.now(timezone.utc),
            cache_expires_at=datetime.now(timezone.utc) + timedelta(days=1),  # Cache valid for 24h
            created_at=datetime.now(timezone.utc)
        )

        analysis = ai_analysis_repository.create(db, analysis)

        if async_generation:
            # Enqueue asynchronous worker in the future releases
            logger.info(f"Asynchronous AI analysis generation queued for IPO: {ipo.company_name} (Version: {analysis.version})")
            return analysis

        # Synchronous execution flow
        try:
            self._run_generation_and_update(db, analysis, ipo)
        except Exception as e:
            logger.error(f"Failed generating AI analysis for {ipo.company_name}: {str(e)}")
            analysis.status = AIAnalysisStatus.FAILED
            db.commit()
            raise AppException("AI Generation failed", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return analysis

    def _run_generation_and_update(self, db: Session, analysis: AIAnalysis, ipo) -> None:
        # Prepare payload
        ipo_details = {
            "price_band": ipo.price_band,
            "lot_size": ipo.lot_size,
            "issue_size": ipo.issue_size,
            "sector": ipo.sector,
            "industry": ipo.industry,
        }
        if ipo.details:
            ipo_details.update({
                "company_overview": ipo.details.company_overview,
                "business_model": ipo.details.business_model,
                "promoters": ipo.details.promoters,
                "objectives": ipo.details.objectives,
                "financial_summary": ipo.details.financial_summary,
            })

        # Run provider generation
        res = self.provider.generate_analysis(ipo.company_name, ipo_details)

        # Map back to model
        analysis.status = AIAnalysisStatus.COMPLETED
        analysis.summary = res["summary"]
        analysis.business_analysis = res["business_analysis"]
        analysis.financial_analysis = res["financial_analysis"]
        analysis.risk_analysis = res["risk_analysis"]
        analysis.management_analysis = res["management_analysis"]
        analysis.valuation_analysis = res["valuation_analysis"]
        analysis.industry_analysis = res["industry_analysis"]
        analysis.structured_data = res["structured_data"]
        
        analysis.financial_score = res["financial_score"]
        analysis.management_score = res["management_score"]
        analysis.industry_score = res["industry_score"]
        analysis.risk_score = res["risk_score"]
        analysis.valuation_score = res["valuation_score"]
        analysis.overall_score = res["overall_score"]
        
        analysis.confidence_score = res["confidence_score"]
        analysis.confidence_reason = res["confidence_reason"]
        
        # Match recommendation enum
        rec_str = res["recommendation"]
        try:
            analysis.recommendation = AIRecommendation(rec_str)
        except ValueError:
            analysis.recommendation = AIRecommendation.NEUTRAL

        analysis.provider = res["provider"]
        analysis.model_name = res["model_name"]
        analysis.prompt_version = res["prompt_version"]
        analysis.tokens_used = res["tokens_used"]
        analysis.processing_time_ms = res["processing_time_ms"]
        
        db.commit()

ai_analysis_service = AIAnalysisService()
