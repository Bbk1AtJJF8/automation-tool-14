import json
import os

def load_config(file_path, defaults):
    if not os.path.exists(file_path):
        return defaults
    with open(file_path, 'r') as config_file:
        try:
            config = json.load(config_file)
        except json.JSONDecodeError:
            return defaults
    combined_config = defaults.copy()
    combined_config.update(config)
    return combined_config

# Default configuration values
DEFAULTS = {
    'host': 'localhost',
    'port': 8080,
    'debug': False,
}

# Example of loading configuration
config = load_config('config.json', DEFAULTS)

if __name__ == '__main__':
    print(config)  # For demo purposes