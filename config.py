import json
import os

class ConfigLoader:
    def __init__(self, default_file='defaults.json', user_file='config.json'):
        self.default_file = default_file
        self.user_file = user_file
        self.config = self.load_config()

    def load_config(self):
        defaults = self.load_json(self.default_file)
        user_config = self.load_json(self.user_file) or {}
        return {**defaults, **user_config}

    def load_json(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                return json.load(file)
        return {}

    def get(self, key, default=None):
        return self.config.get(key, default)

loader = ConfigLoader()

if __name__ == '__main__':
    print(loader.config)
    print(loader.get('some_key', 'default_value'))