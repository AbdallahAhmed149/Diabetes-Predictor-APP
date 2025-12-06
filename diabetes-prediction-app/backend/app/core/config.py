import os
from pydantic_settings import BaseSettings
from typing import List, Union


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Diabetes Prediction API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/diabetes_db"

    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # CORS
    # Can be set as environment variable (comma-separated string) or will use localhost default
    BACKEND_CORS_ORIGINS: Union[List[str], str] = ["http://localhost:3000", "http://localhost:8000"]
    
    @property
    def cors_origins(self) -> List[str]:
        """Parse CORS origins from environment variable or use defaults"""
        if isinstance(self.BACKEND_CORS_ORIGINS, str):
            # If it's a string from env var, split by comma and strip whitespace
            origins = [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",")]
            return origins
        return self.BACKEND_CORS_ORIGINS

    # ML Models
    ML_MODELS_PATH: str = os.path.join(
        os.path.dirname(__file__), "..", "..", "ml_models"
    )

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
