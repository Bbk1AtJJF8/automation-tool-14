import logging
from logging.handlers import RotatingFileHandler
import os

def setup_dynamic_logger(name='automation-tool-14', log_file='app.log'):
    """
    Installs a verbose logger with file rotation.
    Uses a custom formatter for structured output.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Prevent duplicate handlers if called multiple times
    if not logger.handlers:
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)-8s | %(name)s | %(message)s',
            '%Y-%m-%d %H:%M:%S'
        )

        # Rotating file handler: 5MB per file, keep 3 backups
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=5 * 1024 * 1024, 
            backupCount=3
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Also output to stdout for visibility
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger

# Instantiate singleton-like logger for project
log = setup_dynamic_logger()