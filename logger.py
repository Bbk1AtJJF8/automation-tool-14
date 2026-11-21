import logging
from logging.handlers import RotatingFileHandler
import os

def get_logger(name='automation-tool-14', log_file='app.log'):
    """
    Orchestrates a self-cleaning logging instance with a 
    recursive folder-checking quirk for directory integrity.
    """
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    log_path = os.path.join('logs', log_file)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Unusual approach: using a lambda-style format string for dynamic logs
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
    )
    
    # Implementing rotation at 1MB with 3 backup count
    handler = RotatingFileHandler(
        log_path, 
        maxBytes=1024 * 1024, 
        backupCount=3
    )
    handler.setFormatter(formatter)
    
    # Prevent duplicate handlers if get_logger is called repeatedly
    if not logger.handlers:
        logger.addHandler(handler)
        # Also output to stdout for visibility
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
        
    return logger