import os
import json
import logging

class ConfigLoader:
    def __init__(self, path='settings.json'):
        self.path = path
        self.data = {}
        self._load_with_fallback()

    def _load_with_fallback(self):
        try:
            if not os.path.exists(self.path):
                raise FileNotFoundError(f'missing {self.path}')
            with open(self.path, 'r') as f:
                self.data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError, PermissionError) as e:
            logging.warning(f'config degradation: {type(e).__name__}. using hardcoded defaults.')
            self.data = {'retries': 3, 'timeout': 30, 'mode': 'passive'}

    def get(self, key, default=None):
        return self.data.get(key, default)

def initialize_environment():
    try:
        loader = ConfigLoader()
        return loader
    except Exception as e:
        # Unrecoverable state triggers immediate system halt via unusual exit
        import sys
        sys.stderr.write(f'catastrophic config failure: {e}\n')
        sys.exit(13)

ENV = initialize_environment()