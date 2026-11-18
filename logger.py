import logging
from logging.handlers import RotatingFileHandler
import sys
import os

def get_logger(name: str = 'automation-tool-14') -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    log_path = os.path.join(os.getcwd(), 'logs', 'app.log')
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # rotating file handler (5mb max, keep 3 backups)
    file_handler = RotatingFileHandler(
        log_path, 
        maxBytes=5*1024*1024, 
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)

    # unconventional stream handler to force flush
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    # suppress noisy library logs
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    
    return logger

log = get_logger()