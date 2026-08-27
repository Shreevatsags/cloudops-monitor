from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.application import Application
from app.models.deployment import Deployment
from app.models.deployment_log import DeploymentLog
from app.models.user import User
from app.utils.security import get_current_user
from app.services.docker_service import deploy_docker_container
from app.services.docker_service import (
    stop_docker_container,
    start_docker_container
)

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
            DeploymentLog.deployment_id == deployment.id
        )
        .order_by(
            DeploymentLog.timestamp.asc()
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
    # 1. Find application and verify ownership
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

    # 2. Make sure the application has been built
    if not application.docker_image:
        raise HTTPException(
            status_code=400,
            detail="Application must be built before deployment"
        )

    # 3. Create deployment record
    deployment = Deployment(
        application_id=application.id,
        version="v1.0",
        status="pending"
    )

    db.add(deployment)
    db.commit()
    db.refresh(deployment)

    # 4. Create initial log
    db.add(
        DeploymentLog(
            deployment_id=deployment.id,
            message="Deployment started"
        )
    )

    db.commit()

    # 5. Generate unique container information
    container_name = (
        f"cloudops-app-{application.id}-"
        f"deployment-{deployment.id}"
    )

    host_port = 9000 + deployment.id

    try:

        db.add(
            DeploymentLog(
                deployment_id=deployment.id,
                message="Starting Docker container"
            )
        )

        db.commit()

        # 6. Start Docker container
        result = deploy_docker_container(
            image_name=application.docker_image,
            container_name=container_name,
            host_port=host_port
        )

        container_id = result["container_id"]
        deployment.container_id = container_id
        deployment.container_name = container_name
        deployment.host_port = host_port

        # 7. Save deployment logs
        db.add(
            DeploymentLog(
                deployment_id=deployment.id,
                message=f"Container started: {container_id}"
            )
        )

        db.add(
            DeploymentLog(
                deployment_id=deployment.id,
                message=f"Application available on port {host_port}"
            )
        )

        # 8. Mark deployment successful
        deployment.status = "success"

        db.add(
            DeploymentLog(
                deployment_id=deployment.id,
                message="Deployment completed successfully"
            )
        )

        db.commit()
        db.refresh(deployment)

        return {
            "id": deployment.id,
            "application_id": deployment.application_id,
            "version": deployment.version,
            "status": deployment.status,
            "container_id": container_id,
            "container_name": container_name,
            "host_port": host_port,
            "message": "Deployment completed successfully"
        }

    except Exception as error:

        deployment.status = "failed"

        db.add(
            DeploymentLog(
                deployment_id=deployment.id,
                message=f"Deployment failed: {str(error)}"
            )
        )

        db.commit()

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

@router.post("/{deployment_id}/stop")
def stop_deployment(
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

    if not deployment.container_name:
        raise HTTPException(
            status_code=400,
            detail="Container information not available"
        )

    try:

        result = stop_docker_container(
            deployment.container_name
        )

        deployment.status = "stopped"

        db.commit()
        db.refresh(deployment)

        return {
            "message": "Deployment stopped successfully",
            "deployment_id": deployment.id,
            "status": deployment.status,
            "container_name": deployment.container_name
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

@router.post("/{deployment_id}/restart")
def restart_deployment(
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

    if not deployment.container_name:
        raise HTTPException(
            status_code=400,
            detail="Container information not available"
        )

    try:

        result = start_docker_container(
            deployment.container_name
        )

        deployment.status = "success"

        db.commit()
        db.refresh(deployment)

        return {
            "message": "Deployment restarted successfully",
            "deployment_id": deployment.id,
            "status": deployment.status,
            "container_name": deployment.container_name
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )