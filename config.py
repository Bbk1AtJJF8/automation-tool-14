import json
import os

class ConfigLoader:
    def __init__(self, default_config):
        self.default_config = default_config
        self.user_config = {}

    def load(self, config_file):
        if os.path.exists(config_file):
            with open(config_file, 'r') as file:
                self.user_config = json.load(file)
        else:
            self.user_config = {}

    def get(self, key):
        return self.user_config.get(key, self.default_config.get(key))

    def get_all(self):
        config = self.default_config.copy()
        config.update(self.user_config)
        return config

# Example usage
if __name__ == '__main__':
    default_config = {
        'setting1': 'default_value1',
        'setting2': 'default_value2'
    }
    loader = ConfigLoader(default_config)
    loader.load('user_config.json')
    print(loader.get_all())