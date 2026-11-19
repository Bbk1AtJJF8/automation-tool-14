import logging
from logging.handlers import RotatingFileHandler
import os

def get_logger(name='automation-tool-14', log_file='app.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(process)d | %(message)s'
        )
        
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=1024 * 1024 * 5, 
            backupCount=3
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger

class ContextLogger:
    def __init__(self, name):
        self.log = get_logger(name)

    def __enter__(self):
        self.log.info('--- session start ---')
        return self.log

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.log.error(f'session failed: {exc_val}')
        self.log.info('--- session end ---')