import os

import pytest
from invoke_containers.env import get_boolean


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("t", True),
        ("true", True),
        ("y", True),
        ("yes", True),
        ("1", True),
        ("f", False),
        ("false", False),
        ("n", False),
        ("no", False),
        ("0", False),
    ],
)
def test_get_boolean(value, expected):
    name = "TEST"
    os.environ[name] = value
    assert get_boolean(name) == expected


def test_get_boolean_can_raise_on_missing():
    name = "TEST"
    i = 0
    while os.environ.get(name) is not None:
        i += 1
        name = f"TEST{i}"

    with pytest.raises(ValueError):
        get_boolean(name, missing_is_error=True)
