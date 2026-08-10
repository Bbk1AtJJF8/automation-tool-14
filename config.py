import json
import os

class ConfigLoader:
    DEFAULTS = {
        'host': 'localhost',
        'port': 8080,
        'debug': False,
        'timeout': 30,
    }

    def __init__(self, config_file=None):
        self.config = self.DEFAULTS.copy()
        if config_file and os.path.exists(config_file):
            self.load_config(config_file)

    def load_config(self, config_file):
        with open(config_file, 'r') as f:
            file_config = json.load(f)
            self.config.update(file_config)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value

    def __repr__(self):
        return json.dumps(self.config, indent=4)

# Example usage
if __name__ == '__main__':
    loader = ConfigLoader('config.json')
    print(loader)