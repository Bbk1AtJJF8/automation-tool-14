import json
import os

DEFAULT_CONFIG = {
    'log_level': 'INFO',
    'max_connections': 10,
    'timeout': 30,
    'retry_attempts': 3
}

class ConfigLoader:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as file:
                try:
                    custom_config = json.load(file)
                    return {**DEFAULT_CONFIG, **custom_config}
                except json.JSONDecodeError:
                    print('Error decoding JSON file. Using defaults.')
        return DEFAULT_CONFIG

    def get(self, key):
        return self.config.get(key, None)

    def __repr__(self):
        return json.dumps(self.config, indent=2)
