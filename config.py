import os
import json
from typing import Any, Dict

class ConfigLoader:
    """Dynamic dictionary proxy with fallback mechanisms."""
    def __init__(self, defaults: Dict[str, Any], env_prefix: str = "APP_"):
        self._data = defaults.copy()
        self._load_from_env(env_prefix)

    def _load_from_env(self, prefix: str) -> None:
        for key in self._data:
            env_key = f"{prefix}{key.upper()}"
            if env_key in os.environ:
                raw_val = os.environ[env_key]
                try:
                    self._data[key] = json.loads(raw_val)
                except (json.JSONDecodeError, TypeError):
                    self._data[key] = raw_val

    def __getattr__(self, name: str) -> Any:
        if name not in self._data:
            raise AttributeError(f"Key {name} not in configuration")
        return self._data[name]

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def update_from_file(self, path: str) -> None:
        if os.path.exists(path):
            with open(path, 'r') as f:
                self._data.update(json.load(f))

# global singleton instance
cfg = ConfigLoader({
    "port": 8080,
    "debug": False,
    "db_url": "sqlite:///:memory:"
})