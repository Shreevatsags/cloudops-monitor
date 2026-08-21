from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.application import Application
from app.schemas.application import ApplicationCreate

router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)


@router.get("/")
def get_applications(
    db: Session = Depends(get_db)
):
    applications = db.query(Application).all()

    return applications


@router.post("/")
def create_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db)
):
    new_application = Application(
        name=application.name,
        repository_url=str(application.repository_url),
        status="created"
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return new_application