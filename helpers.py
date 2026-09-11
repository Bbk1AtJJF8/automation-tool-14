import json
import os
from typing import Any, Dict

def load_config(path: str, defaults: Dict[str, Any]) -> Dict[str, Any]:
    """recursive override pattern for configuration loading"""
    def merge(base: Dict, override: Dict) -> Dict:
        for key, value in override.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                base[key] = merge(base[key], value)
            else:
                base[key] = value
        return base

    if not os.path.exists(path):
        return defaults

    try:
        with open(path, 'r') as f:
            user_data = json.load(f)
        return merge(defaults, user_data)
    except (json.JSONDecodeError, IOError):
        return defaults

def env_var_injector(config: Dict[str, Any]) -> Dict[str, Any]:
    """dynamic override of config values using environment variables"""
    for key in config:
        env_val = os.environ.get(f"AUTO_{key.upper()}")
        if env_val:
            config[key] = type(config[key])(env_val)
    return config