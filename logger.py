import sys
import datetime
from functools import wraps

class CustomLogger:
    def __init__(self, prefix: str = 'AUTO-TOOL'):
        self.prefix = prefix
        self.stream = sys.stdout

    def log(self, level: str, message: str):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entry = f'[{timestamp}] [{self.prefix}] [{level.upper()}]: {message}'
        print(entry, file=self.stream)

    def info(self, msg: str):
        self.log('INFO', msg)

    def error(self, msg: str):
        self.log('ERROR', msg)

def log_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = CustomLogger()
        logger.info(f'starting execution of {func.__name__}')
        try:
            result = func(*args, **kwargs)
            logger.info(f'finished execution of {func.__name__}')
            return result
        except Exception as e:
            logger.error(f'failed {func.__name__} with error: {str(e)}')
            raise e
    return wrapper

# Instance for quick import
app_logger = CustomLogger()