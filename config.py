import os
import json
from typing import Any, Dict, Optional
class Config:
    def __init__(self, config_dict: Optional[Dict[str, Any]] = None, json_path: Optional[str] = None):
        self._defaults = {"timeout": 30, "retries": 3, "debug": False, "max_items": 100}
        self._data = self._defaults.copy()
        try:
            if json_path:
                self._load_from_json(json_path)
            elif config_dict:
                self._merge_config(config_dict)
            else:
                self._load_from_environment()
        except Exception as e:
            self._handle_init_error(e)
    def _load_from_json(self, path: str):
        try:
            with open(path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            if not isinstance(loaded, dict):
                raise ValueError("Config must be JSON object")
            self._merge_config(loaded)
        except FileNotFoundError:
            pass
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON: {exc}") from exc
        except PermissionError:
            raise ValueError("Permission error on config file")
    def _merge_config(self, new_config: Dict[str, Any]):
        for key, value in new_config.items():
            if key not in self._defaults:
                if value is not None and (not isinstance(value, str) or value.strip()):
                    self._data[key] = value
                continue
            try:
                if isinstance(self._defaults[key], bool):
                    self._data[key] = str(value).lower() in {"true", "1", "yes"}
                elif isinstance(self._defaults[key], int):
                    self._data[key] = int(value)
                else:
                    self._data[key] = value
            except (ValueError, TypeError):
                pass
    def _load_from_environment(self):
        prefix = "AUTOMATION_"
        for env_key, env_val in os.environ.items():
            if env_key.startswith(prefix):
                key = env_key[len(prefix):].lower()
                if key in self._data:
                    try:
                        if isinstance(self._defaults.get(key), bool):
                            self._data[key] = env_val.lower() in {"true", "1", "yes"}
                        elif isinstance(self._defaults.get(key), int):
                            self._data[key] = int(env_val)
                        else:
                            self._data[key] = env_val
                    except (ValueError, TypeError):
                        pass
    def _handle_init_error(self, error: Exception):
        self._data = self._defaults.copy()
        self._data["_init_error"] = str(error)
    def get(self, key: str, default: Optional[Any] = None) -> Any:
        if key not in self._data:
            if default is not None:
                return default
            raise KeyError(f"Missing config key: {key}")
        val = self._data[key]
        return default if val is None and default is not None else val
    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            raise AttributeError
        try:
            return self.get(name)
        except KeyError:
            raise AttributeError(f"Config attribute {name} missing")
    def to_dict(self) -> Dict[str, Any]:
        return self._data.copy()