import os
import json
from typing import Any, Dict

class ConfigNode:
    def __init__(self, data: Dict[str, Any], defaults: Dict[str, Any], prefix: str = "AUTO_"):
        self._data = data or {}
        self._defaults = defaults or {}
        self._prefix = prefix
        self._cache = {}

    def __getattr__(self, name: str) -> Any:
        if name.startswith('_'):
            raise AttributeError(name)
        if name in self._cache:
            return self._cache[name]

        env_key = f"{self._prefix}{name.upper()}"
        env_val = os.environ.get(env_key)
        
        raw_val = env_val if env_val is not None else self._data.get(name)
        fallback = self._defaults.get(name)

        if isinstance(raw_val, dict) or isinstance(fallback, dict):
            merged_data = {**(fallback or {}), **(raw_val or {})}
            resolved = ConfigNode(merged_data, fallback or {}, prefix=f"{env_key}_")
        elif raw_val is not None:
            if isinstance(raw_val, str) and raw_val.lower() in ('true', 'false'):
                resolved = raw_val.lower() == 'true'
            elif isinstance(raw_val, str) and raw_val.isdigit():
                resolved = int(raw_val)
            else:
                resolved = raw_val
        else:
            resolved = fallback

        self._cache[name] = resolved
        return resolved

DEFAULTS = {
    "timeout": 45,
    "max_retries": 5,
    "agent_name": "auto-bot-14",
    "features": {
        "auto_clean": True,
        "verbose": False
    }
}

class Configuration(ConfigNode):
    def __init__(self, filepath: str = "config.json"):
        data = {}
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
            except