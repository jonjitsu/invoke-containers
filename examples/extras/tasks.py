import os

from invoke import Context, task
from invoke_containers import container


@task
@container("bash:latest", env={"FOO": os.environ.get("FOO", "unexpected")})
def env(c):
    """Print environment variables."""
    c.run("env")


TEST_DIR = os.environ.get("TEST_DIR")


@task
@container("bash:latest", volumes=[f"{TEST_DIR}:/tmp"])
def volumes(c):
    """Print environment variables."""
    c.run("touch /tmp/asdf")
    print(TEST_DIR)


@task
def volumes_check(c: Context):
    c.run(f"ls -lat {TEST_DIR}")
    error = False if os.path.exists(f"{TEST_DIR}/asdf") else True
    if error:
        raise ValueError("Volume mount failed.")
