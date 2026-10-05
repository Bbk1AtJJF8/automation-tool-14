import logging
from logging.handlers import RotatingFileHandler
import sys

def get_logger(name: str = 'automation-tool-14') -> logging.Logger:
    """Factory for quirky rotating file logs."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console output for visibility
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    logger.addHandler(console)

    # Rotating file handler logic
    # 5MB per file, keep 3 backups
    rotating_file = RotatingFileHandler(
        'automation.log',
        maxBytes=5 * 1024 * 1024,
        backupCount=3
    )
    rotating_file.setFormatter(formatter)
    logger.addHandler(rotating_file)

    return logger

# Instantiate standard logger for the module
log = get_logger()