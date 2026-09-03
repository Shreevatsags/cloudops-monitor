from datetime import datetime, timezone

from kubernetes import client, config
from kubernetes.client.rest import ApiException


def load_kubernetes_config():
    """
    Load Kubernetes configuration.

    When running inside EKS, use the pod's in-cluster configuration.
    When running locally, fall back to the user's kubeconfig.
    """
    try:
        config.load_incluster_config()
    except config.ConfigException:
        config.load_kube_config()


def create_application_deployment(
    deployment_name: str,
    image_name: str,
    container_port: int = 8000,
):
    load_kubernetes_config()

    apps_v1 = client.AppsV1Api()

    deployment = client.V1Deployment(
        metadata=client.V1ObjectMeta(
            name=deployment_name,
            labels={
                "app": deployment_name
            },
        ),
        spec=client.V1DeploymentSpec(
            replicas=1,
            selector=client.V1LabelSelector(
                match_labels={
                    "app": deployment_name
                }
            ),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(
                    labels={
                        "app": deployment_name
                    }
                ),
                spec=client.V1PodSpec(
                    containers=[
                        client.V1Container(
                            name=deployment_name,
                            image=image_name,
                            image_pull_policy="Always",
                            ports=[
                                client.V1ContainerPort(
                                    container_port=container_port
                                )
                            ],
                        )
                    ]
                ),
            ),
        ),
    )

    try:
        result = apps_v1.create_namespaced_deployment(
            namespace="default",
            body=deployment,
        )

        return {
            "name": result.metadata.name,
            "status": "created",
        }

    except ApiException as error:
        raise RuntimeError(
            f"Failed to create Kubernetes deployment: {error}"
        )


def delete_application_deployment(deployment_name: str):
    load_kubernetes_config()

    apps_v1 = client.AppsV1Api()

    try:
        apps_v1.delete_namespaced_deployment(
            name=deployment_name,
            namespace="default",
            body=client.V1DeleteOptions(),
        )

        return {
            "name": deployment_name,
            "status": "deleted",
        }

    except ApiException as error:
        raise RuntimeError(
            f"Failed to delete Kubernetes deployment: {error}"
        )


def restart_application_deployment(deployment_name: str):
    load_kubernetes_config()

    apps_v1 = client.AppsV1Api()

    try:
        deployment = apps_v1.read_namespaced_deployment(
            name=deployment_name,
            namespace="default",
        )

        if deployment.spec.template.metadata.annotations is None:
            deployment.spec.template.metadata.annotations = {}

        deployment.spec.template.metadata.annotations[
            "cloudops/restarted-at"
        ] = datetime.now(timezone.utc).isoformat()

        apps_v1.patch_namespaced_deployment(
            name=deployment_name,
            namespace="default",
            body=deployment,
        )

        return {
            "name": deployment_name,
            "status": "restarted",
        }

    except ApiException as error:
        raise RuntimeError(
            f"Failed to restart Kubernetes deployment: {error}"
        )