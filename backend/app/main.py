from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine

from app.models import (
    User,
    Application,
    Deployment,
    DeploymentLog
)

from app.routes.auth import router as auth_router
from app.routes.applications import (
    router as applications_router
)


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="CloudOps Monitor API",
    description="Cloud-native DevOps monitoring platform",
    version="1.0.0"
)


# --------------------------------------------------
# CORS Configuration
# --------------------------------------------------

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Routes
# --------------------------------------------------

app.include_router(auth_router)

app.include_router(applications_router)


@app.get("/")
def root():
    return {
        "message": "CloudOps Monitor API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }