import os
from pathlib import Path
from typing import Any, Dict

class AppConfig:
    def __init__(self, env_prefix: str = 'ATOOL'):
        self._env = env_prefix
        self.settings: Dict[str, Any] = {}
        self._load_from_env()

    def _load_from_env(self) -> None:
        base_dir = Path(os.getenv(f'{self._env}_HOME', '/tmp/automation-tool-14'))
        self.settings.update({
            'root': base_dir,
            'logs': base_dir / 'logs',
            'data': base_dir / 'data',
            'timeout': int(os.getenv(f'{self._env}_TIMEOUT', '30')),
            'debug': os.getenv(f'{self._env}_DEBUG', 'false').lower() == 'true'
        })
        for path in [self.settings['logs'], self.settings['data']]:
            path.mkdir(parents=True, exist_ok=True)

    def __getitem__(self, key: str) -> Any:
        return self.settings.get(key)

    def __repr__(self) -> str:
        return f"<Config loaded from {self.settings['root']}>"

def get_config() -> AppConfig:
    if not hasattr(get_config, '_instance'):
        get_config._instance = AppConfig()
    return get_config._instance

if __name__ == '__main__':
    cfg = get_config()
    print(f'Active config initialized: {cfg}')