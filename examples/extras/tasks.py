import os

from invoke import task
from invoke_containers import container


@task
@container("bash:latest", env={"FOO": os.environ.get("FOO", "unexpected")})
def env(c):
    """Print environment variables."""
    c.run("env")
