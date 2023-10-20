import os
import shutil

from invoke import task
from invoke_containers import container


@container("hashicorp/terraform:1.6")
@task
def version(c):
    """Print the terraform version."""
    c.run(f"terraform version")


@task
@container("hashicorp/terraform:1.6")
def init(c):
    """Initialize terraform."""
    c.run(f"terraform init")


@task
@container("hashicorp/terraform:1.6")
def apply(c):
    """Apply terraform."""
    c.run(f"terraform apply -auto-approve")


@task
@container("hashicorp/terraform:1.6")
def output(c):
    """Print terraform output."""
    c.run(f"terraform output")


@task
def test(c):
    """Run tests."""
    print("testing stub...")


@task
@container("hashicorp/terraform:1.6")
def destroy(c):
    """Destroy terraform."""
    c.run(f"terraform apply -destroy -auto-approve")


@task
def clean(c):
    """Clean up artifacts."""
    shutil.rmtree(".terraform", ignore_errors=True)
    shutil.rmtree("terraform.tfstate", ignore_errors=True)
    artifacts = [
        ".terraform",
        "terraform.tfstate",
        "terraform.tfstate.backup",
        ".terraform.lock.hcl",
    ]
    for artifact in artifacts:
        if os.path.isdir(artifact):
            print(f"removing {artifact}")
            shutil.rmtree(artifact, ignore_errors=True)
        elif os.path.isfile(artifact):
            print(f"removing {artifact}")
            os.unlink(artifact)


@task(version, init, apply, output, test, destroy, clean)
def e2e(c):
    """End to end test."""


if __name__ == "__main__":
    from invoke import Collection, Program

    program = Program(
        name="Invoke",
        binary="inv[oke]",
        binary_names=["invoke", "inv"],
        version="0.0.0",
    )
    program.run()
