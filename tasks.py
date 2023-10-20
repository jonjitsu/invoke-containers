from typing import Optional

from invoke import task
from invoke_containers import container


@task
def test_examples(c):
    """Test all examples."""
    c.run("pytest -vv tests/examples/")


@task(test_examples)
def test(c):
    """Run all tests."""


@task
def ufmt(c):
    """Format code."""
    c.run("ufmt format")


@task
def mypy(c):
    """Run mypy."""
    c.run("mypy src tests")


@task
def lint(c):
    """Lint code."""
    c.run("ufmt check")
