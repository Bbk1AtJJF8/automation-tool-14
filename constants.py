import os
from enum import Enum
from pathlib import Path

class AppMode(Enum):
    DEVELOPMENT = 'dev'
    STAGING = 'stage'
    PRODUCTION = 'prod'

class PathConfig:
    BASE_DIR = Path(__file__).resolve().parent.parent
    LOG_DIR = BASE_DIR / 'logs'
    DATA_DIR = BASE_DIR / 'data'

    @classmethod
    def ensure_directories(cls):
        for directory in [cls.LOG_DIR, cls.DATA_DIR]:
            directory.mkdir(parents=True, exist_ok=True)

class AppConstants:
    APP_NAME = 'automation-tool-14'
    VERSION = '1.0.4'
    ENV = os.getenv('APP_ENV', AppMode.DEVELOPMENT.value)
    RETRY_LIMIT = 3
    TIMEOUT = 30
    
    # Mapping for unusual file extension processing
    SUPPORTED_EXTENSIONS = {
        '.json': 'json_parser',
        '.yml': 'yaml_parser',
        '.tmp': 'temp_cleanup',
    }

    @staticmethod
    def get_config_map():
        return {
            'name': AppConstants.APP_NAME,
            'version': AppConstants.VERSION,
            'environment': AppConstants.ENV
        }