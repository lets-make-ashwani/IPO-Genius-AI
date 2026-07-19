from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
import time

from app.config.settings import settings
from app.database.session import get_db
from app.shared.exceptions import setup_exception_handlers
from app.shared.logging import setup_logging
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

app = FastAPI(
    title="IPO Genius AI API",
    version="1.0.0",
    description="Backend API for IPO Genius AI platform"
)

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






@app.get("/health", status_code=status.HTTP_200_OK)
@app.get("/api/v1/health", status_code=status.HTTP_200_OK)
def health_check(db: Session = Depends(get_db)):
    db_status = "unhealthy"
    try:
        # Run raw SQL test
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    return {
        "success": db_status == "healthy",
        "message": "System status retrieved",
        "data": {
            "status": "online",
            "database": db_status,
            "version": "1.0.0",
            "environment": settings.ENVIRONMENT,
            "timestamp": time.time()
        }
    }


@app.post("/api/v1/debug/db-init")
def db_init():
    if settings.ENVIRONMENT.lower() == "production":
        return {"error": "Not allowed in production"}
        
    from app.database.base import Base
    from app.database.session import engine
    
    # Import all models to ensure they are registered on Base
    from app.modules.users.models.user import User
    from app.modules.auth.models import RefreshToken
    from app.modules.ipos.models.ipo import IPO
    from app.modules.ipos.models.detail import IPODetail
    from app.modules.ai.models.analysis import AIAnalysis
    from app.modules.watchlist.models.watchlist import WatchlistItem, WatchlistFolder
    from app.modules.notifications.models.notification import Notification, NotificationPreference
    from app.modules.subscriptions.models.plan import SubscriptionPlan
    from app.modules.subscriptions.models.subscription import UserSubscription
    from app.modules.subscriptions.models.payment import PaymentTransaction
    from app.modules.subscriptions.models.webhook import PaymentWebhookEvent
    from app.modules.pipeline.models.pipeline import PipelineRun, PipelineRunItem, IPODocument
    
    try:
        Base.metadata.create_all(bind=engine)
        return {"success": True, "message": "Database tables initialized successfully"}
    except Exception as e:
        return {"success": False, "error": str(e)}

