import json
import os

class ConfigLoader:
    def __init__(self, default_config_path='default_config.json'):
        self.default_config_path = default_config_path
        self.config = self.load_config()

    def load_config(self):
        config = self.load_defaults()
        user_config_path = os.getenv('CONFIG_PATH', 'user_config.json')
        if os.path.exists(user_config_path):
            user_config = self.load_user_config(user_config_path)
            config.update(user_config)
        return config

    def load_defaults(self):
        with open(self.default_config_path, 'r') as f:
            return json.load(f)

    def load_user_config(self, user_config_path):
        with open(user_config_path, 'r') as f:
            return json.load(f)

if __name__ == '__main__':
    loader = ConfigLoader()
    print(loader.config)