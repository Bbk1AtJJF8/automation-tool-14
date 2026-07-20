import os
from typing import Dict, Any

def load_config(file_path: str) -> Dict[str, Any]:
    """
    Load configuration from a given file path.

    Args:
        file_path (str): The path to the configuration file.

    Returns:
        Dict[str, Any]: A dictionary containing configuration settings.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'Configuration file not found: {file_path}')
    with open(file_path, 'r') as file:
        return {line.split('=')[0].strip(): line.split('=')[1].strip() for line in file if '=' in line}

CONFIG_PATH = os.getenv('CONFIG_PATH', 'default_config.ini')
CONFIG = load_config(CONFIG_PATH)

if __name__ == '__main__':
    print(CONFIG)