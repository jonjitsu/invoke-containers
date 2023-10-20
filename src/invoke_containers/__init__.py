import os
import shlex
import shutil
from functools import lru_cache, wraps
from typing import Any, Callable, Dict, Optional, Union

from invoke import Context, Local
from invoke.tasks import Task

from invoke_containers import env


@lru_cache
def discover_container_program(environ: Optional[Dict[str, str]] = None) -> str:
    """
    Figure out which container program to use. Allow specifying a program
    via the env.CONTAINER_PROGRAM environment variable.
    env.CONTAINER_PROGRAM can be a relative or absolute path to a
    program or the name of a program that can be found on the path.
    """
    if environ is None:
        environ = dict(os.environ)

    maybe_program: Optional[str] = environ.get(env.CONTAINER_PROGRAM)
    if maybe_program:
        if os.path.exists(maybe_program):
            return maybe_program
        resolved_program = shutil.which(maybe_program)
        if resolved_program:
            return resolved_program
        raise ValueError(
            f"{env.CONTAINER_PROGRAM} points to {maybe_program} which doesn't exist or is not on the path."
        )

    possible_programs = ["podman", "docker"]
    for possible_program in possible_programs:
        program = shutil.which(possible_program)
        if program:
            return program
    raise ValueError(
        f"Could not find any of the following programs on the path: {possible_programs}"
        f"Please install one of them or set the {env.CONTAINER_PROGRAM} environment variable."
    )


class ContainerRunner(Local):
    """
    pyinvoke seems to hardcode the runner to a local runner. Create a local
    runner that uses a container program instead of the local shell.

    Can we support something like a remote docker daemon?
    """

    def start(self, command: str, shell: str, env: Dict[str, Any]) -> None:
        proxy = self.context.config.container.proxy
        container_program = discover_container_program()
        work_dir = "/work"
        cwd = os.getcwd()
        cmd = [
            container_program,
            "run",
            "--rm",
            f"--volume={cwd}:{work_dir}",
            f"--workdir={work_dir}",
            "--entrypoint",
            "/bin/sh",
        ]
        if self.using_pty:
            cmd.append("-it")
        cmd += [
            proxy.image,
            "-c",
            command,
        ]
        proxy_command = " ".join(shlex.quote(part) for part in cmd)
        super().start(proxy_command, shell, env)


def create_proxy(func: Callable, container_proxy: "ContainerProxy") -> Callable:
    @wraps(func)
    def proxy(c: Context, *args, **kwargs):
        c.config.runners.local = ContainerRunner
        if "container" not in c.config:
            c.config.container = {}
        c.config.container.proxy = container_proxy
        return func(c, *args, **kwargs)

    return proxy


class ContainerProxy:
    """
    @ContainerProxy("go:1.20")
    @task
    def build(c):
        c.run("go build -o myapp")
    """

    def __init__(self, image: Optional[str] = None):
        self.image = image

    def __call__(self, image: Union[Callable, Task], *args, **kwargs):
        """"""
        if isinstance(image, Task):
            image.body = create_proxy(image.body, self)
            return image
        return create_proxy(image, self)


container = ContainerProxy
