import os
from pathlib import Path
from subprocess import PIPE, Popen
from typing import Dict, Optional, Tuple, Union

TESTING_DIR = Path(__file__).parent
SRC_DIR = TESTING_DIR.parent
PROJECT_ROOT_DIR = SRC_DIR.parent
EXAMPLES_DIR = PROJECT_ROOT_DIR / "examples"


class Example:
    """An example "invoker"."""

    def __init__(self, example_name: str):
        self.example_name = example_name
        self.example_dir = EXAMPLES_DIR / example_name

    def run(
        self,
        *args,
        await_completion: bool = True,
        env_overrides: Optional[Dict[str, str]] = None,
    ) -> Union[Popen, Tuple[int, str, str]]:
        env = os.environ.copy()
        env.update(env_overrides or {})
        process = Popen(
            ["inv"] + list(args),
            cwd=self.example_dir,
            stdout=PIPE,
            stderr=PIPE,
            env=env,
        )
        if await_completion:
            stdout, stderr = process.communicate()
            return process.returncode, stdout.decode(), stderr.decode()
        else:
            return process

    def invoke(
        self,
        task_name: str,
        await_completion: bool = True,
        env_overrides: Optional[Dict[str, str]] = None,
    ) -> Union[Popen, Tuple[int, str, str]]:
        """Invoke a task in the example directory using subprocess."""
        return self.run(
            task_name, await_completion=await_completion, env_overrides=env_overrides
        )
