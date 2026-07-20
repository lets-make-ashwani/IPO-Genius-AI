import logging
from datetime import datetime, timezone
from app.database.session import SessionLocal
from app.modules.pipeline.services.pipeline import pipeline_service
from app.modules.pipeline.models.pipeline import PipelineRunTrigger

logger = logging.getLogger("app")

try:
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    from apscheduler.triggers.cron import CronTrigger
    pipeline_scheduler = AsyncIOScheduler()
except ImportError:
    pipeline_scheduler = None
    logger.warning("[APScheduler] apscheduler package not installed. Automated background scheduling disabled.")

def run_scheduled_pipeline_job():
    """
    Background job triggered by APScheduler.
    Executes automated data discovery across NSE, BSE, and InvestorGain.
    """
    logger.info("[APScheduler] Starting scheduled hourly IPO pipeline execution")
    db = SessionLocal()
    try:
        idempotency_key = f"cron_{datetime.now(timezone.utc).strftime('%Y%m%d_%H')}"
        
        for provider in ["NSE", "INVESTORGAIN"]:
            try:
                pkey = f"{idempotency_key}_{provider}"
                logger.info(f"[APScheduler] Triggering automated run for provider: {provider}")
                pipeline_service.execute_pipeline_run(
                    db=db,
                    provider_name=provider,
                    trigger=PipelineRunTrigger.SCHEDULED,
                    idempotency_key=pkey
                )
            except Exception as e:
                logger.warning(f"[APScheduler] Run skipped or failed for {provider}: {e}")
    finally:
        db.close()

def start_pipeline_scheduler():
    """Starts the background APScheduler worker if available."""
    if pipeline_scheduler is not None and not pipeline_scheduler.running:
        try:
            pipeline_scheduler.add_job(
                run_scheduled_pipeline_job,
                trigger=CronTrigger(minute=0),
                id="hourly_ipo_pipeline_job",
                replace_existing=True
            )
            pipeline_scheduler.start()
            logger.info("[APScheduler] IPO Pipeline Scheduler successfully started")
        except Exception as e:
            logger.error(f"[APScheduler] Failed to start pipeline scheduler: {e}")

def shutdown_pipeline_scheduler():
    """Gracefully shuts down the background APScheduler worker if available."""
    if pipeline_scheduler is not None and pipeline_scheduler.running:
        try:
            pipeline_scheduler.shutdown(wait=False)
            logger.info("[APScheduler] IPO Pipeline Scheduler shut down")
        except Exception as e:
            logger.error(f"[APScheduler] Error during scheduler shutdown: {e}")
