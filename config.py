import json
import os
from collections import ChainMap
from pathlib import Path
from typing import Any, Dict, Union


class ConfigLoader:
    """Dynamic configuration loader using ChainMap and dynamic attribute lookup."""

    DEFAULT_CONFIG: Dict[str, Any] = {
        "app_name": "automation-tool-14",
        "debug": False,
        "max_workers": 4,
        "timeout": 30.0,
        "log_level": "INFO",
        "retry_attempts": 3,
    }

    def __init__(self, config_path: Union[str, Path, None] = None):
        self._path = Path(config_path) if config_path else None
        self._user_config = self._load_file()
        self._env_config = self._load_env()
        # Prioritizes: Environment variables > File config > Default fallbacks
        self._store = ChainMap(self._env_config, self._user_config, self.DEFAULT_CONFIG)

    def _load_file(self) -> Dict[str, Any]:
        if self._path and self._path.is_file():
            try:
                with open(self._path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def _load_env(self) -> Dict[str, Any]:
        env_data = {}
        prefix = "APP_"
        for key, val in os.environ.items():
            if key.startswith(prefix):
                clean_key = key[len(prefix) :].lower()
                if val.lower() in ("true", "false"):
                    env_data[clean_key] = val.lower() == "true"
                elif val.isdigit():
                    env_data[clean_key] = int(val)
                else:
                    env_data[clean_key] = val
        return env_data

    def get(self, key: str, default: Any = None) -> Any:
        return self._store.get(key, default)

    def __getattr__(self, name: str) -> Any:
        if name in self._store:
            return self._store[name]
        raise AttributeError(f"Configuration option '{name}' not found")

    def __getitem__(self, item: str) -> Any:
        return self._store[item]

    def __repr__(self) -> str:
        return f"ConfigLoader(active_keys={list(self._store.keys())})"