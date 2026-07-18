import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    PORT: int = 8000
    
    # Database Settings
    DATABASE_URL: str
    
    # Security Settings
    JWT_SECRET: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS Settings
    FRONTEND_URL: str = "http://localhost:3000"

    # Payment Settings
    PAYMENT_PROVIDER: str = "MOCK"
    RAZORPAY_KEY_ID: str = ""
    RAZORPAY_KEY_SECRET: str = ""
    RAZORPAY_WEBHOOK_SECRET: str = ""

    # Pipeline Settings
    PIPELINE_PROVIDER: str = "MOCK"
    DOCUMENT_PARSER_PROVIDER: str = "MOCK"
    DOCUMENT_STORAGE_TYPE: str = "LOCAL"
    DOCUMENT_STORAGE_PATH: str = "./pipeline_docs"
    PIPELINE_AI_AUTO_TRIGGER: bool = True
    PIPELINE_MAX_RETRIES: int = 3

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    def __init__(self, **values):
        super().__init__(**values)
        if self.ENVIRONMENT.lower() == "production" and self.PAYMENT_PROVIDER.upper() == "MOCK":
            raise ValueError("Production environment does not allow MOCK payment provider!")

settings = Settings()

