import json
from collections import defaultdict

class ConfigLoader:
    def __init__(self, default_config):
        self.default_config = default_config
        self.user_config = defaultdict(lambda: None)

    def load_config(self, config_file):
        try:
            with open(config_file, 'r') as f:
                user_config = json.load(f)
                self.user_config.update(user_config)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f'Error loading config: {e}')

    def get_config(self, key):
        return self.user_config.get(key, self.default_config.get(key))

if __name__ == '__main__':
    defaults = {'host': 'localhost', 'port': 8080, 'debug': False}
    config_loader = ConfigLoader(defaults)
    config_loader.load_config('settings.json')
    print(config_loader.get_config('host'))  # Example usage
    print(config_loader.get_config('port'))  # Example usage