import os
import json

def load_config(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Config file not found: {file_path}")
    try:
        with open(file_path, 'r') as config_file:
            config = json.load(config_file)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON: {str(e)}")
    
    if 'settings' not in config:
        raise KeyError("'settings' key missing in config")
    
    return config['settings']

if __name__ == '__main__':
    try:
        settings = load_config('config.json')
        print('Loaded settings:', settings)
    except Exception as e:
        print(f'Failed to load config: {str(e)}')
