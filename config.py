import os
import logging
from logging.handlers import RotatingFileHandler

LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = 'app.log'

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

# Create a file handler that logs even debug messages
handler = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=2)
handler.setLevel(LOG_LEVEL)

# Create formatter and add it to the handler
formatter = logging.Formatter(LOG_FORMAT)
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

# Example function to demonstrate logging

def log_example():
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')

if __name__ == '__main__':
    log_example()