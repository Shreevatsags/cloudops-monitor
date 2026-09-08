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
    container_port: int = 5000,
):
    load_kubernetes_config()

    apps_v1 = client.AppsV1Api()
    core_v1 = client.CoreV1Api()

    labels = {
        "app": deployment_name
    }

    # ============================================================
    # KUBERNETES DEPLOYMENT
    # ============================================================

    deployment = client.V1Deployment(
        metadata=client.V1ObjectMeta(
            name=deployment_name,
            labels=labels,
        ),
        spec=client.V1DeploymentSpec(
            replicas=1,
            selector=client.V1LabelSelector(
                match_labels=labels
            ),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(
                    labels=labels
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
                            env=[
                                client.V1EnvVar(name="MYSQL_HOST", value="mysql-service"),
                                client.V1EnvVar(name="MYSQL_USER", value="root"),
                                client.V1EnvVar(name="MYSQL_PASSWORD", value="root"),
                                client.V1EnvVar(name="MYSQL_DB", value="devops"),
                            ],
                        )
                    ]
                ),
            ),
        ),
    )

    # ============================================================
    # KUBERNETES SERVICE
    # ============================================================

    service_name = f"{deployment_name}-service"

    service = client.V1Service(
        metadata=client.V1ObjectMeta(
            name=service_name,
            labels=labels,
        ),
        spec=client.V1ServiceSpec(
            type="LoadBalancer",
            selector=labels,
            ports=[
                client.V1ServicePort(
                    port=80,
                    target_port=container_port,
                    protocol="TCP",
                )
            ],
        ),
    )

    try:

        # Create Deployment
        deployment_result = apps_v1.create_namespaced_deployment(
            namespace="default",
            body=deployment,
        )

        # Create Service
        service_result = core_v1.create_namespaced_service(
            namespace="default",
            body=service,
        )

        return {
            "name": deployment_result.metadata.name,
            "service_name": service_result.metadata.name,
            "status": "created",
        }

    except ApiException as error:

        # If Deployment was created but Service failed,
        # remove the Deployment so we don't leave partial resources.
        try:
            apps_v1.delete_namespaced_deployment(
                name=deployment_name,
                namespace="default",
                body=client.V1DeleteOptions(),
            )
        except Exception:
            pass

        raise RuntimeError(
            f"Failed to create Kubernetes deployment/service: {error}"
        )


def delete_application_deployment(deployment_name: str):
    load_kubernetes_config()

    apps_v1 = client.AppsV1Api()
    core_v1 = client.CoreV1Api()

    service_name = f"{deployment_name}-service"

    try:

        # Delete Service first
        try:
            core_v1.delete_namespaced_service(
                name=service_name,
                namespace="default",
                body=client.V1DeleteOptions(),
            )
        except ApiException as service_error:
            # 404 means the Service is already gone.
            if service_error.status != 404:
                raise

        # Delete Deployment
        apps_v1.delete_namespaced_deployment(
            name=deployment_name,
            namespace="default",
            body=client.V1DeleteOptions(),
        )

        return {
            "name": deployment_name,
            "service_name": service_name,
            "status": "deleted",
        }

    except ApiException as error:
        raise RuntimeError(
            f"Failed to delete Kubernetes deployment/service: {error}"
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