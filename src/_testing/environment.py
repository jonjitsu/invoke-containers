import os
from contextlib import AbstractContextManager
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Self


class Environment(AbstractContextManager):
    def __init__(self):
        self.environ = os.environ.copy()

    def create_executable(self, name: str):
        bin = self.temppath / name
        bin.touch()
        bin.chmod(0o755)

    def __enter__(self) -> Self:
        self.tempdir = TemporaryDirectory()
        self.temppath = Path(self.tempdir.name)
        os.environ["PATH"] = self.tempdir.name
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.tempdir.cleanup()
