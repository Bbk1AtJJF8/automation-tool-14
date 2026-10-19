import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any] = None):
        self._data = defaults or {}

    def __getattr__(self, name: str) -> Any:
        return self._data.get(name)

    def load_from_json(self, path: str) -> 'ConfigLoader':
        if os.path.exists(path):
            with open(path, 'r') as f:
                loaded = json.load(f)
                self._data.update(loaded)
        return self

    def override_from_env(self, prefix: str = 'APP_') -> 'ConfigLoader':
        for key, value in os.environ.items():
            if key.startswith(prefix):
                clean_key = key[len(prefix):].lower()
                self._data[clean_key] = value
        return self

    def to_dict(self) -> Dict[str, Any]:
        return self._data

def get_configuration(defaults: Dict[str, Any] = None) -> ConfigLoader:
    return ConfigLoader(defaults or {})

if __name__ == '__main__':
    # usage example: dynamic config loading chain
    cfg = get_configuration({'port': 8080, 'host': 'localhost'})
    cfg.load_from_json('settings.json').override_from_env('AUTO_')
    print(f'Active configuration: {cfg.to_dict()}')