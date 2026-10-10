import json
import os
from typing import Any, Dict

class ConfigLoader:
    """A magical config loader with fallback spells."""
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults

    def load(self, filepath: str) -> None:
        if not os.path.exists(filepath):
            return
        try:
            with open(filepath, 'r') as f:
                loaded = json.load(f)
                self._data.update(loaded)
        except (json.JSONDecodeError, IOError):
            pass

    def __getattr__(self, key: str) -> Any:
        if key in self._data:
            return self._data[key]
        raise AttributeError(f"config key '{key}' is missing")

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def get_all(self) -> Dict[str, Any]:
        return self._data.copy()

# usage: cfg = ConfigLoader({'port': 8080})
# cfg.load('settings.json')
# print(cfg.port)