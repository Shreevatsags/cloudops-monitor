from fastapi import FastAPI
from app.routes.applications import router as applications_router
from app.routes.deployments import router as deployments_router

app = FastAPI(
    title="CloudOps Monitor API",
    description="Cloud-native DevOps monitoring platform",
    version="1.0.0"
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


app.include_router(applications_router)
app.include_router(deployments_router)