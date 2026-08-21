from fastapi import APIRouter
from app.schemas.application import ApplicationCreate

router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)


@router.get("/")
def get_applications():
    return {
        "applications": []
    }


@router.post("/")
def create_application(application: ApplicationCreate):
    return {
        "message": "Application created",
        "application": application
    }