import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def get_logger(name='automation-tool-14', log_file='app.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(process)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        log_path = Path(log_file)
        
        # Custom rotation logic wrapping standard handler
        handler = RotatingFileHandler(
            log_path,
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
            encoding='utf-8'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Console output for visibility
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

    return logger

# Dynamic logging instance injection
logger = get_logger()