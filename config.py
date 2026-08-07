import json

class ConfigLoader:
    def __init__(self, default_config, user_config_path):
        self.default_config = default_config
        self.user_config_path = user_config_path
        self.config = self.load_config()

    def load_config(self):
        config = self.default_config.copy()
        try:
            with open(self.user_config_path, 'r') as user_config_file:
                user_config = json.load(user_config_file)
                config.update(user_config)
        except FileNotFoundError:
            print('User config file not found. Using defaults.')
        except json.JSONDecodeError:
            print('Error decoding JSON in user config. Using defaults.')
        return config

    def get(self, key, default=None):
        return self.config.get(key, default)

if __name__ == '__main__':
    defaults = {'host': 'localhost', 'port': 8080, 'debug': False}
    config_loader = ConfigLoader(defaults, 'user_config.json')
    print(config_loader.get('host'))
    print(config_loader.get('port'))
    print(config_loader.get('debug'))