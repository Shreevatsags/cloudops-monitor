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
from app.services.docker_service import build_docker_image
from app.services.git_service import clone_repository

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
# BUILD DOCKER IMAGE
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

    repository_path = None

    image_name = f"cloudops-app:{application.id}"

    try:

        # 1. Clone GitHub repository
        repository_path = clone_repository(
            application.repository_url
        )

        # 2. Build Docker image
        result = build_docker_image(
            project_path=repository_path,
            image_name=image_name
        )

        # 3. Save Docker image name
        application.docker_image = image_name
        application.status = "built"

        db.commit()
        db.refresh(application)

        return {
            "message": "Docker image built successfully",
            "image": image_name,
            "output": result["output"]
        }

    except Exception as error:

        application.status = "build_failed"

        db.commit()

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    finally:

        # 4. Remove temporary repository
        if repository_path:

            import shutil

            shutil.rmtree(
                repository_path,
                ignore_errors=True
            )