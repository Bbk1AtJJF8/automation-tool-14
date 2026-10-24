import json
import os
from typing import Any, Dict

class ConfigLoader:
    """A dictionary-like object that recursively fetches keys with fallback support."""
    def __init__(self, defaults: Dict[str, Any]):
        self._store = defaults

    def load(self, path: str) -> None:
        if os.path.exists(path):
            with open(path, 'r') as f:
                user_cfg = json.load(f)
                self._deep_merge(self._store, user_cfg)

    def _deep_merge(self, base: Dict, patch: Dict) -> None:
        for k, v in patch.items():
            if isinstance(v, dict) and k in base and isinstance(base[k], dict):
                self._deep_merge(base[k], v)
            else:
                base[k] = v

    def get(self, key_path: str, default: Any = None) -> Any:
        keys = key_path.split('.')
        curr = self._store
        try:
            for k in keys:
                curr = curr[k]
            return curr
        except (KeyError, TypeError):
            return default

    def __getitem__(self, key: str) -> Any:
        return self._store[key]

    @property
    def raw(self) -> Dict[str, Any]:
        return self._store