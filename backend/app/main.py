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
