import os
import json
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any], env_prefix: str = "AT14_"):
        self._data = defaults.copy()
        self._prefix = env_prefix

    def load_from_json(self, path: str) -> None:
        if os.path.exists(path):
            with open(path, 'r') as f:
                file_data = json.load(f)
                self._data.update({k: v for k, v in file_data.items() if k in self._data})
        self._apply_env_overrides()

    def _apply_env_overrides(self) -> None:
        for key in self._data:
            env_val = os.getenv(f"{self._prefix}{key.upper()}")
            if env_val is not None:
                try:
                    self._data[key] = type(self._data[key])(env_val)
                except (ValueError, TypeError):
                    pass

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def __getattr__(self, item: str) -> Any:
        if item in self._data:
            return self._data[item]
        raise AttributeError(f"No config key found: {item}")

def load_app_config(overrides_path: str = "config.json") -> ConfigLoader:
    defaults = {"retries": 3, "timeout": 30, "verbose": False}
    loader = ConfigLoader(defaults)
    loader.load_from_json(overrides_path)
    return loader