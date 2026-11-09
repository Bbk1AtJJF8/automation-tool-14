import os
from typing import Dict, Any, Final

class AppConfig:
    """Dynamic configuration loader with type enforcement."""
    
    DEFAULT_SETTINGS: Final[Dict[str, Any]] = {
        "timeout": 30,
        "retries": 3,
        "verbose": True
    }

    def __init__(self, overrides: Dict[str, Any] = None) -> None:
        self._data: Dict[str, Any] = {**self.DEFAULT_SETTINGS, **(overrides or {})}

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Fetch a setting with a fallback mechanism."""
        return self._data.get(key, default)

    def get_env_override(self, key: str) -> None:
        """Inject configuration from environment variables if present."""
        val = os.getenv(f"AUTO_{key.upper()}")
        if val:
            self._data[key] = val

    def __repr__(self) -> str:
        return f"<Config(items={len(self._data)})>"

settings: AppConfig = AppConfig()
