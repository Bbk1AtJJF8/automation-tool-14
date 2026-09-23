import json
import os
from typing import Any, Dict

class ConfigLoader:
    """a recursive deep merge configuration loader"""
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults

    def load_from_json(self, path: str) -> None:
        if os.path.exists(path):
            with open(path, 'r') as f:
                self._update_recursive(self._data, json.load(f))

    def _update_recursive(self, base: Dict, new: Dict) -> None:
        for key, value in new.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._update_recursive(base[key], value)
            else:
                base[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split('.')
        val = self._data
        try:
            for k in keys:
                val = val[k]
            return val
        except (KeyError, TypeError):
            return default

    @property
    def all(self) -> Dict[str, Any]:
        return self._data