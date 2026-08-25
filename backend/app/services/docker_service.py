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