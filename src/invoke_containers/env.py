import os

# Environment variables namespace
NS = "CONTAINER_INVOKE"
# Which container program to use
CONTAINER_PROGRAM = f"{NS}_PROGRAM"
# Provides a mechanism for not running the tasks in containers
INVOKE_ON_HOST = f"{NS}_ON_HOST"


def get_boolean(var_name: str, missing_is_error: bool = False) -> bool:
    """
    Get a boolean value from an environment variable.
    """
    value = os.environ.get(var_name)
    if value is None:
        if missing_is_error:
            raise ValueError(f"Environment variable {var_name} not set.")
        value = "false"

    return value.lower() in ["true", "1", "t", "y", "yes"]
