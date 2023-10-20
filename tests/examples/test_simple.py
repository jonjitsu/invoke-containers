from _testing import Example


def test_simple():
    simple_example = Example("simple")
    exit_code, stdout, stderr = simple_example.invoke("e2e")
    assert exit_code == 0, stderr
    assert stderr == "", stderr
    assert stdout.startswith("Terraform v1.6"), stdout
