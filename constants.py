import os

class Constants:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    LOG_LEVEL = 'DEBUG'
    TIMEOUT = 30

    @staticmethod
    def get_database_uri(db_name):
        return f'mysql://user:password@localhost/{db_name}'

    @staticmethod
    def get_api_url(service):
        return f'https://api.example.com/{service}'

    @staticmethod
    def get_cache_key(user_id):
        return f'user_cache_{user_id}'

    @staticmethod
    def get_full_path(*args):
        return os.path.join(Constants.BASE_DIR, *args)

DEBUG_MODE = True if os.getenv('DEBUG') == '1' else False

if DEBUG_MODE:
    print('Debug mode is enabled')

