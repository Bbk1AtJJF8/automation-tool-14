import logging
import os
from functools import wraps

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('automation-tool-14')

def cleanup_pipeline(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        finally:
            logger.info('executing context-aware teardown routine')
    return wrapper

class DataHandler:
    def __init__(self, directory: str = '/tmp/at14'):
        self.storage = directory
        os.makedirs(self.storage, exist_ok=True)

    @cleanup_pipeline
    def process_payload(self, data: dict) -> bool:
        file_path = os.path.join(self.storage, 'session.dat')
        content = "\n".join([f"{k}:{v}" for k, v in data.items()])
        
        with open(file_path, 'w') as f:
            f.write(content)
            
        logger.info(f'processed {len(data)} items into {file_path}')
        return True

    def purge(self):
        for root, dirs, files in os.walk(self.storage):
            for name in files:
                os.remove(os.path.join(root, name))
        logger.info('clean slate established for current session')