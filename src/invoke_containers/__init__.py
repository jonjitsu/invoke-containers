import os
import shlex
import shutil
from functools import wraps
from typing import Any, Callable, Dict, Optional, Union

from invoke import Context, Local
from invoke.tasks import Task

from invoke_containers import env


def discover_container_program() -> str:
    """
    Figure out which container program to use. Allow specifying a program
    via the env.CONTAINER_PROGRAM environment variable.
    env.CONTAINER_PROGRAM can be a relative or absolute path to a
    program or the name of a program that can be found on the path.
    """
    maybe_program: Optional[str] = os.environ.get(env.CONTAINER_PROGRAM)
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


def create_docker_env_options(env: Dict[str, str]):
    return [f"-e{key}={value}" for key, value in env.items()]


class ContainerRunner(Local):
    """
    pyinvoke seems to hardcode the runner to a local runner. Create a local
    runner that uses a container program instead of the local shell.

    Can we support something like a remote docker daemon?
    """

    def start(self, command: str, shell: str, env: Dict[str, Any]) -> None:
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
        cmd.extend(create_docker_env_options(self.context.config.container.env))
        cmd += [
            self.context.config.container.image,
            "-c",
            command,
        ]
        proxy_command = " ".join(shlex.quote(part) for part in cmd)
        super().start(proxy_command, shell, env)


def container(image: str, env: Optional[Dict] = None) -> Callable:
    """
    Run invoke tasks in a container.

    Example usage:
    @task
    @container("go:1.20")
    def build(c):
        c.run("go build -o myapp")
    """
    if env is None:
        env = {}

    def create_proxy(func: Callable) -> Callable:
        """
        Proxy the invoke task execution in order to override the runner
        with a container runner. Store configuration for the container
        runner on the config object.
        """

        @wraps(func)
        def proxy(c: Context, *args, **kwargs):
            c.config.runners.local = ContainerRunner
            if "container" not in c.config:
                c.config.container = {}
            c.config.container.image = image
            c.config.container.env = env
            return func(c, *args, **kwargs)

        return proxy

    def decorator(task: Union[Callable, Task]):
        """
        Make adjustments depending on if the @container decorator is
        used before or after the @task decorator.

        If @container is used before @task decorator then we receive a
        Task object and need to proxy the task.body which is where the
        users function is stored.
        """
        if isinstance(task, Task):
            task.body = create_proxy(task.body)
            return task
        return create_proxy(task)

    return decorator
