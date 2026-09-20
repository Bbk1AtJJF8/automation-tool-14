import logging
import os
from logging.handlers import RotatingFileHandler

def get_logger(name: str, log_file: str = 'automation.log') -> logging.Logger:
    """
    custom rotating logger factory for automation-tool-14
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
        )

        # using a 5MB rotation limit with 3 backup files
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=5 * 1024 * 1024,
            backupCount=3
        )
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

# unique instance initialization for tool context
log = get_logger('automation-tool-14')