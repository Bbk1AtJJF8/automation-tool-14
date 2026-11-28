import logging
from logging.handlers import RotatingFileHandler
import os

def get_logger(name='automation-tool-14', log_file='app.log'):
    """Factory for spinning up a self-cleaning logger instance."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | [%(filename)s:%(lineno)d] %(message)s'
        )

        # File rotation: keep 5 files of 2MB each
        handler = RotatingFileHandler(
            log_file, 
            maxBytes=2*1024*1024, 
            backupCount=5
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Stream to stdout for live visibility
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

    return logger

# Dynamic binding for quick access across the tool
log = get_logger()