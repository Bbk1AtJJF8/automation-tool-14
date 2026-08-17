import json
import os

class ConfigLoader:
    def __init__(self, default_config=None):
        if default_config is None:
            default_config = {}
        self.default_config = default_config
        self.loaded_config = self.default_config.copy()

    def load_from_file(self, filepath):
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f'Configuration file not found: {filepath}')
        with open(filepath, 'r') as file:
            config_data = json.load(file)
            self.loaded_config.update(config_data)

    def get(self, key, fallback=None):
        return self.loaded_config.get(key, fallback)

    def set(self, key, value):
        self.loaded_config[key] = value

    def save_to_file(self, filepath):
        with open(filepath, 'w') as file:
            json.dump(self.loaded_config, file, indent=4)

# Example usage:
# loader = ConfigLoader({'default_key': 'default_value'})
# loader.load_from_file('config.json')
# print(loader.get('some_key', 'fallback_value'))