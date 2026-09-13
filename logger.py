import logging
from logging.handlers import RotatingFileHandler
import sys

def get_logger(name='automation-tool-14', log_file='app.log'):
    """
    A somewhat aggressive logger setup that wraps standard streams
    into rotating file chunks to keep the disk clean.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
    )

    # Rolling files: 2MB max, keeping 5 historical backups
    handler = RotatingFileHandler(
        log_file, 
        maxBytes=2*1024*1024, 
        backupCount=5
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Also echo to stdout because visibility is good
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    logger.addHandler(console)

    # Prevent duplicate handlers if re-called
    if not logger.handlers[1:]:
        logger.propagate = False
    
    return logger

log = get_logger()