from fastapi import FastAPI

from app.database import Base, engine

# Import models so SQLAlchemy knows about them
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
Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="CloudOps Monitor API",
    description="Cloud-native DevOps monitoring platform",
    version="1.0.0"
)


app.include_router(
    auth_router
)

app.include_router(
    applications_router
)


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