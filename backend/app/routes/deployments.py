from fastapi import APIRouter

router = APIRouter(
    prefix="/deployments",
    tags=["Deployments"]
)


@router.get("/")
def get_deployments():
    return {
        "deployments": []
    }


@router.post("/")
def create_deployment():
    return {
        "message": "Deployment started"
    }