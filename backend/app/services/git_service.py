import shutil
import subprocess
import tempfile


def clone_repository(repository_url: str) -> str:

    temp_dir = tempfile.mkdtemp(
        prefix="cloudops-build-"
    )

    try:

        result = subprocess.run(
            [
                "git",
                "clone",
                "--depth",
                "1",
                repository_url,
                temp_dir
            ],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:

            shutil.rmtree(
                temp_dir,
                ignore_errors=True
            )

            raise RuntimeError(
                result.stderr
            )

        return temp_dir

    except Exception:

        shutil.rmtree(
            temp_dir,
            ignore_errors=True
        )

        raise