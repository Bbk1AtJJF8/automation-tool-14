import json
import os

class ConfigLoader:
    def __init__(self, default_config_path):
        self.default_config_path = default_config_path
        self.config = self.load_defaults()

    def load_defaults(self):
        with open(self.default_config_path) as f:
            return json.load(f)

    def load_from_file(self, config_file):
        if os.path.exists(config_file):
            with open(config_file) as f:
                user_config = json.load(f)
            self.config.update(user_config)
        else:
            print(f'Warning: {config_file} not found. Using defaults.')

    def get(self, key, default=None):
        return self.config.get(key, default)

# Example usage:
# default_config = ConfigLoader('default_config.json')
# default_config.load_from_file('user_config.json')
# print(default_config.get('some_key', 'default_value'))