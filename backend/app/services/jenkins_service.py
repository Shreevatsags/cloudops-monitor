import os
import requests


JENKINS_URL = os.getenv("JENKINS_URL")
JENKINS_USER = os.getenv("JENKINS_USER")
JENKINS_API_TOKEN = os.getenv("JENKINS_API_TOKEN")


def trigger_jenkins_build(application_id: int, repository_url: str):
    if not JENKINS_URL:
        raise RuntimeError("JENKINS_URL is not configured")

    if not JENKINS_USER:
        raise RuntimeError("JENKINS_USER is not configured")

    if not JENKINS_API_TOKEN:
        raise RuntimeError("JENKINS_API_TOKEN is not configured")

    url = (
        f"{JENKINS_URL}/job/CloudOps-Monitor-CI-CD/buildWithParameters"
    )

    params = {
        "APPLICATION_ID": str(application_id),
        "REPOSITORY_URL": repository_url,
    }

    response = requests.post(
        url,
        params=params,
        auth=(JENKINS_USER, JENKINS_API_TOKEN),
        timeout=30,
    )

    if response.status_code not in (200, 201, 202):
        raise RuntimeError(
            f"Jenkins build trigger failed: "
            f"{response.status_code} {response.text}"
        )

    return {
        "status": "triggered",
        "message": "Jenkins build triggered successfully",
    }