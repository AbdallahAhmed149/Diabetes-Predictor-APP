from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import Base, engine
from app.api.endpoints import auth, patients, predictions
from app.ml.load_models import get_ml_models

# Load models globally
try:
    print("Loading ML models globally...")
    get_ml_models()
    print("ML models loaded successfully!")
except Exception as e:
    print(f"Warning: Could not preload models: {e}")
    
# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth")
app.include_router(patients.router, prefix="/api/patients")
app.include_router(predictions.router, prefix="/api/predictions")


@app.on_event("startup")
async def startup_event():
    """Load ML models on startup"""
    print("🚀 Starting Diabetes Prediction API...")
    get_ml_models()  # Load models
    print("✅ Application ready!")


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Diabetes Prediction API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


