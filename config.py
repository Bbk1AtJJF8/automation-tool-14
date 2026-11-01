import os
import json
import logging

class ConfigLoader:
    def __init__(self, path):
        self.path = path
        self.data = {}

    def load(self):
        try:
            if not os.path.exists(self.path):
                raise FileNotFoundError(f'config missing: {self.path}')
            with open(self.path, 'r') as f:
                raw = f.read()
                self.data = json.loads(raw) if raw else {}
        except (json.JSONDecodeError, FileNotFoundError, PermissionError) as e:
            self._fallback_recovery(e)
        return self.data

    def _fallback_recovery(self, error):
        logging.error(f'config corruption detected: {error}. defaulting to safe mode.')
        self.data = {'mode': 'safe', 'retries': 3, 'timeout': 30}

    def get(self, key, default=None):
        return self.data.get(key, default)

def get_app_config():
    loader = ConfigLoader('settings.json')
    return loader.load()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    cfg = get_app_config()
    print(f'current config: {cfg}')