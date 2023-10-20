import os

import pytest

from _testing.environment import Environment
from invoke_containers import as_volume_strs, discover_container_program
from invoke_containers.env import CONTAINER_PROGRAM


def test_discover_container_program_finds_docker_on_the_path():
    with Environment() as environment:
        environment.create_executable("docker")
        print(os.environ["PATH"])
        print(os.listdir(environment.temppath))
        assert os.path.basename(discover_container_program()) == "docker"


def test_discover_container_program_finds_podman_on_the_path():
    with Environment() as environment:
        environment.create_executable("podman")
        print(os.environ["PATH"])
        print(os.listdir(environment.temppath))
        assert os.path.basename(discover_container_program()) == "podman"


def test_discover_container_program_uses_CONTAINER_PROGRAM_env_var_abspath():
    with Environment() as environment:
        bin = "container-exec"
        environment.create_executable(bin)
        os.environ[CONTAINER_PROGRAM] = str(environment.temppath / bin)
        assert discover_container_program() == os.environ[CONTAINER_PROGRAM]


def test_discover_container_program_uses_CONTAINER_PROGRAM_env_var_on_path():
    with Environment() as environment:
        bin = "container-exec"
        environment.create_executable(bin)
        os.environ[CONTAINER_PROGRAM] = bin
        assert discover_container_program() == str(environment.temppath / bin)


@pytest.mark.parametrize(
    ("volumes", "expected"),
    [
        (["/src:/dest"], ["/src:/dest"]),
        (["/src:/dest:ro"], ["/src:/dest:ro"]),
        ({"/src": "/dest:ro"}, ["/src:/dest:ro"]),
        ({"/src": ("/dest", "ro")}, ["/src:/dest:ro"]),
        ([("/src", "/dest")], ["/src:/dest"]),
        ([("/src", "/dest", "ro")], ["/src:/dest:ro"]),
    ],
)
def test_as_volume_strs(volumes, expected):
    assert as_volume_strs(volumes) == expected
