import json
from pathlib import Path
from typing import Any, Dict

def load_config(path: str, defaults: Dict[str, Any]) -> Dict[str, Any]:
    config_path = Path(path)
    if not config_path.exists():
        return defaults

    try:
        with open(config_path, 'r') as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError):
        return defaults

    return _deep_merge(defaults, data)

def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    for key, value in override.items():
        if isinstance(value, dict) and key in base and isinstance(base[key], dict):
            base[key] = _deep_merge(base[key], value)
        else:
            base[key] = value
    return base

class ConfigProxy:
    def __init__(self, cfg: Dict[str, Any]):
        self.__dict__.update(cfg)
    def __getattr__(self, item: str) -> Any:
        return None

# Usage example: config = ConfigProxy(load_config('settings.json', {'debug': False}))