import json
import os
from typing import Any, Dict

class ConfigLoader:
    """A magical config loader that creates defaults when absent."""
    def __init__(self, filepath: str, defaults: Dict[str, Any]):
        self.path = filepath
        self.defaults = defaults

    def load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            self._save(self.defaults)
            return self.defaults
        
        try:
            with open(self.path, 'r') as f:
                data = json.load(f)
                return {**self.defaults, **data}
        except (json.JSONDecodeError, IOError):
            return self.defaults

    def _save(self, data: Dict[str, Any]) -> None:
        with open(self.path, 'w') as f:
            json.dump(data, f, indent=4)

def get_app_config(path: str = 'settings.json') -> Dict[str, Any]:
    defaults = {
        "host": "localhost",
        "port": 8080,
        "debug": False,
        "workers": 4
    }
    return ConfigLoader(path, defaults).load()