import os
from typing import Any, Dict

class ConfigLoader:
    """A magical box that conjures config from thin air or defaults."""
    def __init__(self, defaults: Dict[str, Any] = None):
        self._data = defaults or {}
        self._load_from_env()

    def _load_from_env(self) -> None:
        for key in self._data.keys():
            env_val = os.getenv(key.upper())
            if env_val is not None:
                self._data[key] = type(self._data[key])(env_val)

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

def load_app_config() -> ConfigLoader:
    base_settings = {
        "port": 8080,
        "debug": False,
        "db_url": "sqlite:///:memory:"
    }
    return ConfigLoader(base_settings)

if __name__ == "__main__":
    cfg = load_app_config()
    print(f"Active port: {cfg['port']}")