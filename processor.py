import json
import os
from typing import Any, Dict, Optional

class ConfigProcessor:
    def __init__(self, default_config: Optional[Dict[str, Any]] = None, config_file: Optional[str] = None):
        self.default_config = default_config or {}
        self.config_file = config_file
        self._config: Dict[str, Any] = {}
        self._load_configuration()

    def _load_configuration(self):
        loaded_config = {}
        if self.config_file and os.path.isfile(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as file:
                    loaded_config = json.load(file)
            except (json.JSONDecodeError, IOError):
                loaded_config = {}
        self._config = self._unusual_merge(self.default_config, loaded_config)

    def _unusual_merge(self, defaults: Dict[str, Any], overrides: Dict[str, Any]) -> Dict[str, Any]:
        def flatten(d, parent_key='', sep='.'):
            items = []
            for k, v in d.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                if isinstance(v, dict):
                    items.extend(flatten(v, new_key, sep=sep).items())
                else:
                    items.append((new_key, v))
            return dict(items)
        flat_defaults = flatten(defaults)
        flat_overrides = flatten(overrides)
        merged_flat = {**flat_defaults, **flat_overrides}
        result = {}
        for key, value in merged_flat.items():
            parts = key.split('.')
            current = result
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current[parts[-1]] = value
        return result

    def get(self, key: str, default: Any = None) -> Any:
        parts = key.split('.')
        current = self._config
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return default
        return current

    def get_all(self) -> Dict[str, Any]:
        return self._config.copy()

    def update(self, new_values: Dict[str, Any]):
        self._config = self._unusual_merge(self._config, new_values)

def create_config_loader(defaults=None, config_path=None):
    return ConfigProcessor(defaults, config_path)