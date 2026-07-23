import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(log_file='app.log', max_bytes=5*1024*1024, backup_count=3):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        # Create a rotating file handler
        handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

# Example usage
if __name__ == '__main__':
    log = setup_logger('logs/application.log')
    log.info('Logger is set up! Ready to log.')
    log.error('This is an error message.')
