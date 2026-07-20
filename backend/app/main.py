from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
import time
import logging

from app.config.settings import settings
from app.database.session import get_db, SessionLocal
from app.shared.exceptions import setup_exception_handlers
from app.shared.logging import setup_logging
from app.shared.middleware import RequestIDMiddleware
from app.services.database_initializer import DatabaseInitializer, startup_state

from app.modules.auth.routes import router as auth_router
from app.modules.users.routes import router as user_router
from app.modules.ipos.routes import router as ipo_router
from app.modules.ai.routes import router as ai_router
from app.modules.watchlist.routes import router as watchlist_router
from app.modules.notifications.routes import router as notifications_router
from app.modules.admin.routes import router as admin_router
from app.modules.subscriptions.routes import subscription_router, payment_router
from app.modules.pipeline.routes import router as pipeline_router
from fastapi.staticfiles import StaticFiles

# Setup Logging
setup_logging()
logger = logging.getLogger("app")

app = FastAPI(
    title="IPO Genius AI API",
    version=settings.VERSION,
    description="Backend API for IPO Genius AI platform"
)

# Add Request ID Middleware
app.add_middleware(RequestIDMiddleware)

# CORS configuration
origins = [
    settings.FRONTEND_URL,
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup Exception Handlers
setup_exception_handlers(app)

# Mount Static Files for Avatar Uploads
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include Routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")
app.include_router(ipo_router, prefix="/api/v1")
app.include_router(ai_router, prefix="/api/v1")
app.include_router(watchlist_router, prefix="/api/v1")
app.include_router(notifications_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")
app.include_router(subscription_router, prefix="/api/v1")
app.include_router(payment_router, prefix="/api/v1")
app.include_router(pipeline_router, prefix="/api/v1")

@app.on_event("startup")
def on_startup():
    logger.info(f"[Startup] Launching IPO Genius AI v{settings.VERSION} ({settings.APP_ENV})...")
    db = SessionLocal()
    try:
        DatabaseInitializer.initialize(db)
    except Exception as e:
        logger.error(f"[Startup] Database initialization encountered error: {e}")
    finally:
        db.close()

    # Start and verify APScheduler
    try:
        startup_state.status = "STARTING_SCHEDULER"
        from app.modules.pipeline.scheduler.manager import start_pipeline_scheduler
        start_pipeline_scheduler()
        startup_state.status = "READY"
    except Exception as e:
        logger.error(f"[Startup] Scheduler start error: {e}")
        startup_state.status = "READY"


@app.on_event("shutdown")
def on_shutdown():
    from app.modules.pipeline.scheduler.manager import shutdown_pipeline_scheduler
    shutdown_pipeline_scheduler()


@app.get("/health", status_code=status.HTTP_200_OK)
@app.get("/api/v1/health", status_code=status.HTTP_200_OK)
def health_check(db: Session = Depends(get_db)):
    """
    Public health check endpoint.
    """
    db_status = "unhealthy"
    try:
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    return {
        "status": "healthy" if db_status == "healthy" else "unhealthy",
        "success": db_status == "healthy",
        "message": "System status retrieved",
        "data": {
            "status": "online",
            "database": db_status,
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT,
            "timestamp": time.time()
        }
    }
