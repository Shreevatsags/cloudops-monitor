import subprocess


def build_docker_image(
    project_path: str,
    image_name: str
):

    command = [
        "docker",
        "build",
        "-t",
        image_name,
        project_path
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:

        raise RuntimeError(
            result.stderr
        )

    return {
        "image": image_name,
        "output": result.stdout
    }

def deploy_docker_container(
    image_name: str,
    container_name: str,
    host_port: int,
    container_port: int = 8000
):
    command = [
        "docker",
        "run",
        "-d",

        "--name",
        container_name,

        "--network",
        "cloudops-monitor_default",

        "-p",
        f"{host_port}:{container_port}",

        "-e",
        "DATABASE_URL=postgresql://postgres:postgres@cloudops-postgres:5432/cloudops_monitor",

        "-e",
        "JWT_SECRET_KEY=change-this-secret",

        "-e",
        "JWT_ALGORITHM=HS256",

        "-e",
        "JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60",

        image_name
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            result.stderr.strip()
        )

    return {
        "container_id": result.stdout.strip(),
        "output": result.stdout.strip()
    }

def stop_docker_container(container_name: str):

    command = [
        "docker",
        "stop",
        container_name
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            result.stderr.strip()
        )

    return {
        "message": "Container stopped successfully",
        "container_name": container_name
    }


def start_docker_container(container_name: str):

    command = [
        "docker",
        "start",
        container_name
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            result.stderr.strip()
        )

    return {
        "message": "Container started successfully",
        "container_name": container_name
    }