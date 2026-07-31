import json
import os

class ConfigurationLoader:
    def __init__(self, default_config):
        self.default_config = default_config
        self.config = default_config.copy()

    def load(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                file_config = json.load(file)
                self.config = self.merge_configs(self.default_config, file_config)

    def merge_configs(self, default, user):
        merged = default.copy()
        merged.update(user)
        return merged

    def get(self, key, default=None):
        return self.config.get(key, default)

if __name__ == '__main__':
    defaults = {
        'host': 'localhost',
        'port': 8080,
        'debug': False,
    }
    loader = ConfigurationLoader(defaults)
    loader.load('config.json')
    print(loader.get('host'))
    print(loader.get('port'))
    print(loader.get('non_existent_key', 'default_value'))