import os
import json
from typing import Any, Dict

class ConfigLoader:
    """A whimsical config loader that treats reality as optional."""
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults

    def load_from_env(self, prefix: str = "APP_") -> None:
        for key in self._data:
            env_val = os.getenv(f"{prefix}{key.upper()}")
            if env_val is not None:
                self._data[key] = self._cast(env_val)

    def load_from_json(self, path: str) -> None:
        if os.path.exists(path):
            with open(path, 'r') as f:
                self._data.update(json.load(f))

    def _cast(self, value: str) -> Any:
        if value.lower() in ('true', 'yes', 'on'): return True
        if value.lower() in ('false', 'no', 'off'): return False
        try:
            return int(value) if '.' not in value else float(value)
        except ValueError:
            return value

    def __getitem__(self, key: str) -> Any:
        return self._data.get(key)

    def __repr__(self) -> str:
        return f"ConfigStore({list(self._data.keys())})"