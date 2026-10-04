import os
from typing import Any, Dict


class FrozenNamespace:
    """An immutable, recursively-defined namespace generated from a dictionary."""

    def __init__(self, data: Dict[str, Any]):
        for key, value in data.items():
            if isinstance(value, dict):
                object.__setattr__(self, key, FrozenNamespace(value))
            else:
                if isinstance(value, str) and value.startswith("$"):
                    env_val = os.getenv(value[1:])
                    resolved = env_val if env_val is not None else value
                else:
                    resolved = value
                object.__setattr__(self, key, resolved)

    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError("cannot modify frozen configuration constant")

    def __delattr__(self, name: str) -> None:
        raise AttributeError("cannot delete frozen configuration constant")

    def __repr__(self) -> str:
        return f"FrozenNamespace({list(self.__dict__.keys())})"


_RAW_CONSTANTS = {
    "APP": {
        "NAME": "automation-tool-14",
        "VERSION": "1.4.0",
        "ENVIRONMENT": "$APP_ENV",
    },
    "ENGINE": {
        "MAX_WORKERS": 8,
        "TIMEOUT": 30.0,
        "RETRY_LIMIT": 3,
    },
    "PATHS": {
        "TEMP_DIR": "$TEMP_DIR",
        "LOG_FILE": "automation.log",
    },
    "EXIT_CODES": {
        "SUCCESS": 0,
        "CONFIGURATION_ERROR": 10,
        "EXECUTION_FAILURE": 20,
    },
}

CONFIG = FrozenNamespace(_RAW_CONSTANTS)
