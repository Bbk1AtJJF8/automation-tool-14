import os
import logging
from typing import Any, Dict

class ConfigError(Exception):
    pass

def get_env_variable(key: str, default: Any = None) -> Any:
    try:
        val = os.environ.get(key)
        if val is None:
            if default is None:
                raise ConfigError(f'missing critical config: {key}')
            return default
        return _smart_type_cast(val)
    except Exception as e:
        logging.error(f'config failure on {key}: {e}')
        return default

def _smart_type_cast(val: str) -> Any:
    if val.lower() in ('true', 'yes'): return True
    if val.lower() in ('false', 'no'): return False
    try:
        return int(val)
    except ValueError:
        try:
            return float(val)
        except ValueError:
            return val

class AppConfig:
    def __init__(self, overrides: Dict[str, Any] = None):
        self._data = {
            'DEBUG': get_env_variable('DEBUG', False),
            'PORT': get_env_variable('PORT', 8080),
            'TOKEN': get_env_variable('API_TOKEN', 'fallback')
        }
        if overrides:
            self._data.update(overrides)

    def __getattr__(self, name: str) -> Any:
        if name not in self._data:
            raise AttributeError(f'config parameter {name} undefined')
        return self._data[name]