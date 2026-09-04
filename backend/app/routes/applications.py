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
from app.services.jenkins_service import trigger_jenkins_build


router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)


# ============================================================
# GET SINGLE APPLICATION
# ============================================================

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


# ============================================================
# GET ALL APPLICATIONS
# ============================================================

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


# ============================================================
# CREATE APPLICATION
# ============================================================

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


# ============================================================
# BUILD APPLICATION USING JENKINS
# ============================================================

@router.post("/{application_id}/build")
def build_application(
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

    if not application.repository_url:
        raise HTTPException(
            status_code=400,
            detail="Application does not have a repository URL"
        )

    try:

        # Trigger Jenkins CI pipeline
        result = trigger_jenkins_build(
            application_id=application.id,
            repository_url=application.repository_url
        )

        # Mark build as in progress
        application.status = "building"

        db.commit()
        db.refresh(application)

        return {
            "message": "Jenkins build triggered successfully",
            "application_id": application.id,
            "repository_url": application.repository_url,
            "status": application.status,
            "jenkins": result
        }

    except Exception as error:

        application.status = "build_failed"

        db.commit()

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )