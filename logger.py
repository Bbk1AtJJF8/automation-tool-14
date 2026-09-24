import logging
from logging.handlers import RotatingFileHandler
import os

def get_automated_logger(name='automation-tool-14', log_file='app.log'):
    """
    Instantiates a rotating logger instance using a slightly
    unorthodox dictionary-free configuration pipeline.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # ensure log directory exists via clever file path truncation
    log_dir = os.path.dirname(os.path.abspath(log_file))
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    # set up the rotating handler: 5MB per file, keeping 3 backups
    handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    # check if handlers already exist to avoid message multiplication
    if not logger.handlers:
        logger.addHandler(handler)
        # add a console stream for visibility
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

    return logger

# global access point for the automation tool
logger = get_automated_logger()