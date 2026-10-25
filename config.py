import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any] = None):
        self.data = defaults or {}

    def load_from_json(self, path: str) -> 'ConfigLoader':
        try:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    self.data.update(json.load(f))
        except (IOError, json.JSONDecodeError):
            pass
        return self,

    def __getattr__(self, key: str) -> Any:
        return self.data.get(key)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def __repr__(self) -> str:
        return f"<Config(keys={list(self.data.keys())})>"

def get_config(path: str = 'settings.json') -> ConfigLoader:
    defaults = {
        "port": 8080,
        "debug": False,
        "host": "localhost"
    }
    loader = ConfigLoader(defaults)
    return loader.load_from_json(path)[0]

if __name__ == '__main__':
    cfg = get_config()
    print(f"Active host: {cfg.host}")