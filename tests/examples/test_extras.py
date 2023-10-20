from uuid import uuid4

from _testing import Example


def test_extras_env():
    example = Example("extras")
    expected = uuid4().hex

    exit_code, stdout, stderr = example.invoke("env", env_overrides={"FOO": expected})
    assert exit_code == 0, stderr
    assert stderr == "", stderr
    foos = [x for x in stdout.split("\n") if x.startswith("FOO=")]
    assert len(foos) == 1, stdout
    assert foos[0] == f"FOO={expected}", stdout


from tempfile import TemporaryDirectory


def test_extras_volumes():
    example = Example("extras")

    with TemporaryDirectory() as td:
        exit_code, stdout, stderr = example.invoke(
            "volumes", env_overrides={"TEST_DIR": td}
        )
        print(stdout)
        assert exit_code == 0, stderr
        assert stderr == "", stderr

        exit_code, stdout, stderr = example.invoke(
            "volumes-check", env_overrides={"TEST_DIR": td}
        )
        print(stdout)
        assert exit_code == 0, stderr
        assert stderr == "", stderr
