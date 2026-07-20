"""
database_initializer.py — Database Initializer & Startup Orchestrator

Manages application startup state transitions (BOOTSTRAPPING -> SEEDING -> STARTING_SCHEDULER -> READY),
runs transactional bootstrap operations, and queues non-blocking background tasks.
"""

import json
import logging
from typing import Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import inspect

from app.config.settings import settings
from app.modules.ipos.models.ipo import IPO
from app.modules.admin.models.system_metadata import SystemMetadata
from app.services.bootstrap_service import BootstrapService
from app.services.production_seed_service import ProductionSeedService

logger = logging.getLogger("app")

# Global Application Startup State Machine
class AppStartupState:
    status: str = "OFFLINE"
    seeded: bool = False
    version: str = settings.VERSION

startup_state = AppStartupState()

class DatabaseInitializer:
    @staticmethod
    def initialize(db: Session) -> Dict[str, Any]:
        """
        Executes atomic transactional bootstrap & initial database seeding.
        """
        startup_state.status = "BOOTSTRAPPING"
        logger.info("[DatabaseInitializer] Starting application database bootstrap...")

        try:
            # Ensure tables exist in SQLite / development instances
            from app.database.base import Base
            from app.database.session import engine
            Base.metadata.create_all(bind=engine)

            # 1. Ensure Super Admin exists from environment
            BootstrapService.ensure_super_admin(db)

            # 2. Check SystemMetadata seed version
            meta = None
            ipo_count = 0
            try:
                meta = db.query(SystemMetadata).filter(SystemMetadata.key == "production_seed").first()
                ipo_count = db.query(IPO).count()
            except Exception as ex:
                logger.warning(f"[DatabaseInitializer] Metadata query warning: {ex}")

            should_seed = False
            if not meta or ipo_count == 0:
                should_seed = True
            elif meta:
                try:
                    payload = json.loads(meta.value)
                    if payload.get("version") != settings.VERSION and settings.INITIAL_IPO_SEED_ENABLED:
                        should_seed = True
                except Exception:
                    should_seed = True

            result_payload = {}
            if should_seed and settings.INITIAL_IPO_SEED_ENABLED:
                startup_state.status = "SEEDING"
                logger.info("[DatabaseInitializer] Seeding initial IPO dataset...")
                result_payload = ProductionSeedService.seed_ipos(db, seeded_by="startup_bootstrap")
                db.commit()
                startup_state.seeded = True
            else:
                db.commit()
                logger.info(f"[DatabaseInitializer] IPO Records Count: {ipo_count}. Skipping seed.")
                startup_state.seeded = True

            startup_state.status = "READY"
            logger.info("[DatabaseInitializer] Application database bootstrap completed successfully. Status: READY")
            return {
                "status": "READY",
                "seeded": startup_state.seeded,
                "ipo_count": db.query(IPO).count(),
                "meta": result_payload
            }

        except Exception as e:
            db.rollback()
            startup_state.status = "FAILED"
            logger.error(f"[DatabaseInitializer] Bootstrap failed: {e}")
            raise e
