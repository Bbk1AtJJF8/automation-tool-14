import os
import json
from typing import Any, Dict, Optional

DEFAULT_CONFIG: Dict[str, Any] = {
    "timeout": 30,
    "retries": 3,
    "debug": False,
    "max_connections": 10,
    "log_level": "INFO",
    "data_dir": "./data",
    "batch_size": 100,
}

class Config:
    """Configuration loader with defaults and overrides."""

    def __init__(self, config_file: Optional[str] = None) -> None:
        self._data: Dict[str, Any] = DEFAULT_CONFIG.copy()
        if config_file:
            self._load_file(config_file)
        self._apply_env_overrides()

    def _load_file(self, path: str) -> None:
        if os.path.isfile(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    file_data = json.load(f)
                self._deep_merge(self._data, file_data)
            except (json.JSONDecodeError, OSError):
                pass

    def _deep_merge(self, target: Dict[str, Any], source: Dict[str, Any]) -> None:
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._deep_merge(target[key], value)
            else:
                target[key] = value

    def _apply_env_overrides(self) -> None:
        env_prefix = "TOOL_"
        for key, default_val in list(self._data.items()):
            env_key = env_prefix + key.upper()
            if env_key in os.environ:
                env_val = os.environ[env_key]
                if isinstance(default_val, bool):
                    self._data[key] = env_val.lower() in ("true", "1", "yes")
                elif isinstance(default_val, int):
                    try:
                        self._data[key] = int(env_val)
                    except ValueError:
                        pass
                else:
                    self._data[key] = env_val

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        if key not in self._data:
            raise KeyError(f"Config key '{key}' not found")
        return self._data[key]

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"Config has no attribute '{name}'")

    def as_dict(self) -> Dict[str, Any]:
        return self._data.copy()

    def reload(self, config_file: Optional[str] = None) -> None:
        self._data = DEFAULT_CONFIG.copy()
        if config_file:
            self._load_file(config_file)
        self._apply_env_overrides()
