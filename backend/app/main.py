from fastapi import FastAPI

from app.database import engine, Base
from app.routes.applications import router as applications_router
from app.routes.deployments import router as deployments_router

# Import models so SQLAlchemy knows about them
from app.models import User, Application, Deployment, DeploymentLog


app = FastAPI(
    title="CloudOps Monitor API",
    description="Cloud-native DevOps monitoring platform",
    version="1.0.0"
)


# Create database tables
Base.metadata.create_all(bind=engine)


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


# Register API routes
app.include_router(applications_router)
app.include_router(deployments_router)