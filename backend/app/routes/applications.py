from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.application import Application
from app.models.user import User
from app.schemas.application import (
    ApplicationCreate,
    ApplicationResponse
)
from app.utils.security import get_current_user


router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)

@router.get(
    "/{application_id}",
    response_model=ApplicationResponse
)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    application = (
        db.query(Application)
        .filter(
            Application.id == application_id,
            Application.user_id == current_user.id
        )
        .first()
    )

    if application is None:

        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    return application

@router.get(
    "/",
    response_model=list[ApplicationResponse]
)
def get_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    applications = (
        db.query(Application)
        .filter(
            Application.user_id == current_user.id
        )
        .all()
    )

    return applications


@router.post(
    "/",
    response_model=ApplicationResponse
)
def create_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    new_application = Application(
        user_id=current_user.id,
        name=application.name,
        repository_url=application.repository_url,
        status="created"
    )

    db.add(new_application)

    db.commit()

    db.refresh(new_application)

    return new_application