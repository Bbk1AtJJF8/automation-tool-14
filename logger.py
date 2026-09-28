import logging
from logging.handlers import RotatingFileHandler
import os

def get_logger(name='automation-tool-14', log_path='logs/app.log'):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s'
        )
        
        # Creative rotating file handler approach
        handler = RotatingFileHandler(
            log_path, 
            maxBytes=1024 * 1024 * 5, 
            backupCount=3
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Stream for console visibility
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
        
    return logger

# Singleton-ish access instance
log = get_logger()