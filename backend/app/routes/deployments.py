from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.application import Application
from app.models.deployment import Deployment
from app.models.user import User
from app.utils.security import get_current_user
from app.models.deployment_log import DeploymentLog

router = APIRouter(
    prefix="/deployments",
    tags=["Deployments"]
)


@router.get("/")
def get_deployments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deployments = (
        db.query(Deployment)
        .join(
            Application,
            Deployment.application_id == Application.id
        )
        .filter(
            Application.user_id == current_user.id
        )
        .all()
    )

    return deployments

@router.get("/{deployment_id}/logs")
def get_deployment_logs(
    deployment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deployment = (
        db.query(Deployment)
        .join(
            Application,
            Deployment.application_id == Application.id
        )
        .filter(
            Deployment.id == deployment_id,
            Application.user_id == current_user.id
        )
        .first()
    )

    if deployment is None:
        raise HTTPException(
            status_code=404,
            detail="Deployment not found"
        )

    logs = (
        db.query(DeploymentLog)
        .filter(
            DeploymentLog.deployment_id
            == deployment.id
        )
        .all()
    )

    return logs

@router.post("/{application_id}")
def create_deployment(
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

    deployment = Deployment(
        application_id=application.id,
        version="v1.0",
        status="pending"
    )

    db.add(deployment)
    db.commit()
    db.refresh(deployment)

    log = DeploymentLog(
        deployment_id=deployment.id,
        message="Deployment started"
        )

    db.add(log)
    db.commit()

    return deployment