import json
import os
from pathlib import Path
from typing import Any, Dict, Union

DEFAULT_CONFIG: Dict[str, Any] = {
    "app_name": "automation-tool-14",
    "debug": False,
    "max_retries": 3,
    "timeout": 30.0,
    "output_dir": "./output",
    "features": {"auto_cleanup": True, "verbose_logging": False},
}


class ConfigProxy:
    """Creative configuration wrapper supporting dot-access and env overrides."""

    def __init__(
        self,
        defaults: Dict[str, Any],
        filepath: Union[str, Path, None] = None,
        env_prefix: str = "AUTO_",
    ):
        self._data: Dict[str, Any] = defaults.copy()
        self._prefix = env_prefix

        if filepath and Path(filepath).is_file():
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    file_cfg = json.load(f)
                    self._merge(self._data, file_cfg)
            except (json.JSONDecodeError, OSError):
                pass

    def _merge(self, base: Dict[str, Any], overlay: Dict[str, Any]) -> None:
        for key, val in overlay.items():
            if (
                isinstance(val, dict)
                and key in base
                and isinstance(base[key], dict)
            ):
                self._merge(base[key], val)
            else:
                base[key] = val

    def _cast_env(self, raw_val: str, target_type: type) -> Any:
        if target_type is bool:
            return raw_val.lower() in ("true", "1", "yes", "on")
        try:
            return target_type(raw_val)
        except (ValueError, TypeError):
            return raw_val

    def get(self, key: str, default: Any = None) -> Any:
        env_key = f"{self._prefix}{key.upper()}"
        if env_key in os.environ:
            target_type = (
                type(self._data.get(key))
                if key in self._data
                else type(default)
            )
            return self._cast_env(os.environ[env_key], target_type)

        parts = key.split(".")
        val = self._data
        for p in parts:
            if isinstance(val, dict) and p in val:
                val = val[p]
            else:
                return default
        return val

    def __getattr__(self, item: str) -> Any:
        if item.startswith("_"):
            raise AttributeError(item)
        val = self.get(item)
        if val is None:
            raise AttributeError(f"Configuration key '{item}' not found")
        return val

    def __getitem__(self, item: str) -> Any:
        return self.get(item)


def load_config(config_path: Union[str, Path, None] = None) -> ConfigProxy:
    """Instantiate and return the global configuration instance."""
    path = config_path or os.getenv("APP_CONFIG_PATH", "config.json")
    return ConfigProxy(defaults=DEFAULT_CONFIG, filepath=path)
