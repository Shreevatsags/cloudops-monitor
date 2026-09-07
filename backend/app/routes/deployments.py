from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.application import Application
from app.models.deployment import Deployment
from app.models.deployment_log import DeploymentLog
from app.models.user import User
from app.utils.security import get_current_user

from app.services.kubernetes_service import (
    create_application_deployment,
    delete_application_deployment,
    restart_application_deployment,
)


router = APIRouter(
    prefix="/deployments",
    tags=["Deployments"]
)


# ============================================================
# GET ALL DEPLOYMENTS
# ============================================================

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


# ============================================================
# GET SINGLE DEPLOYMENT
# ============================================================

@router.get("/{deployment_id}")
def get_deployment(
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

    kubernetes_deployment_name = deployment.container_name

    kubernetes_service_name = None

    if kubernetes_deployment_name:
        kubernetes_service_name = (
            f"{kubernetes_deployment_name}-service"
        )

    return {
        "id": deployment.id,
        "application_id": deployment.application_id,
        "version": deployment.version,
        "status": deployment.status,
        "container_id": deployment.container_id,
        "container_name": deployment.container_name,
        "host_port": deployment.host_port,
        "kubernetes_deployment": kubernetes_deployment_name,
        "kubernetes_service": kubernetes_service_name,
        "started_at": deployment.started_at,
        "completed_at": deployment.completed_at
    }


# ============================================================
# GET DEPLOYMENT LOGS
# ============================================================

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


# ============================================================
# CREATE KUBERNETES DEPLOYMENT
# ============================================================

@router.post("/{application_id}")
def create_deployment(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # --------------------------------------------------------
    # 1. Find application and verify ownership
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # 2. Make sure application has a Docker image
    # --------------------------------------------------------

    if not application.docker_image:
        raise HTTPException(
            status_code=400,
            detail="Application must have a Docker image before deployment"
        )

    # --------------------------------------------------------
    # 3. Create database deployment record
    # --------------------------------------------------------

    deployment = Deployment(
        application_id=application.id,
        version="v1.0",
        status="pending"
    )

    db.add(deployment)
    db.commit()
    db.refresh(deployment)

    # --------------------------------------------------------
    # 4. Create initial deployment log
    # --------------------------------------------------------

    db.add(
        DeploymentLog(
            deployment_id=deployment.id,
            message="Kubernetes deployment started"
        )
    )

    db.commit()

    # --------------------------------------------------------
    # 5. Generate Kubernetes Deployment name
    # --------------------------------------------------------

    kubernetes_deployment_name = (
        f"cloudops-app-{application.id}-"
        f"deployment-{deployment.id}"
    )

    kubernetes_service_name = (
        f"{kubernetes_deployment_name}-service"
    )

    try:

        db.add(
            DeploymentLog(
                deployment_id=deployment.id,
                message="Creating Kubernetes Deployment and Service"
            )
        )

        db.commit()

        # ----------------------------------------------------
        # 6. Create Kubernetes Deployment + Service
        # ----------------------------------------------------

        result = create_application_deployment(
            deployment_name=kubernetes_deployment_name,
            image_name=application.docker_image,
            container_port=8000
        )

        # ----------------------------------------------------
        # 7. Store Kubernetes Deployment name
        # ----------------------------------------------------

        # Temporary use of existing database field.
        deployment.container_name = kubernetes_deployment_name

        # Kubernetes does not use Docker container ID/host port.
        deployment.container_id = None
        deployment.host_port = None

        # ----------------------------------------------------
        # 8. Log Kubernetes Deployment
        # ----------------------------------------------------

        db.add(
            DeploymentLog(
                deployment_id=deployment.id,
                message=(
                    f"Kubernetes Deployment created: "
                    f"{result['name']}"
                )
            )
        )

        # ----------------------------------------------------
        # 9. Log Kubernetes Service
        # ----------------------------------------------------

        db.add(
            DeploymentLog(
                deployment_id=deployment.id,
                message=(
                    f"Kubernetes Service created: "
                    f"{result['service_name']}"
                )
            )
        )

        # ----------------------------------------------------
        # 10. Mark deployment successful
        # ----------------------------------------------------

        deployment.status = "success"

        db.add(
            DeploymentLog(
                deployment_id=deployment.id,
                message=(
                    "Kubernetes Deployment and Service "
                    "created successfully"
                )
            )
        )

        db.commit()
        db.refresh(deployment)

        return {
            "id": deployment.id,
            "application_id": deployment.application_id,
            "version": deployment.version,
            "status": deployment.status,
            "kubernetes_deployment": kubernetes_deployment_name,
            "kubernetes_service": kubernetes_service_name,
            "docker_image": application.docker_image,
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


# ============================================================
# STOP DEPLOYMENT
# ============================================================

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
            detail="Kubernetes deployment information not available"
        )

    try:

        result = delete_application_deployment(
            deployment.container_name
        )

        deployment.status = "stopped"

        db.add(
            DeploymentLog(
                deployment_id=deployment.id,
                message=(
                    "Kubernetes Deployment and Service deleted"
                )
            )
        )

        db.commit()
        db.refresh(deployment)

        return {
            "message": "Deployment stopped successfully",
            "deployment_id": deployment.id,
            "status": deployment.status,
            "kubernetes_deployment": deployment.container_name,
            "kubernetes_service": result.get("service_name")
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ============================================================
# RESTART DEPLOYMENT
# ============================================================

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
            detail="Kubernetes deployment information not available"
        )

    try:

        restart_application_deployment(
            deployment.container_name
        )

        deployment.status = "success"

        db.add(
            DeploymentLog(
                deployment_id=deployment.id,
                message="Kubernetes Deployment restarted"
            )
        )

        db.commit()
        db.refresh(deployment)

        return {
            "message": "Deployment restarted successfully",
            "deployment_id": deployment.id,
            "status": deployment.status,
            "kubernetes_deployment": deployment.container_name,
            "kubernetes_service": (
                f"{deployment.container_name}-service"
            )
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )