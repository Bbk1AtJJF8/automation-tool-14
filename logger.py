import logging
from logging.handlers import RotatingFileHandler
import sys

def get_logger(name: str = 'automation-tool-14', log_file: str = 'app.log') -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Unusual approach: using a filter to simulate custom coloring for console streams
    class ColorFilter(logging.Filter):
        def filter(self, record):
            record.msg = f'[{record.levelname.lower()}] {record.msg}'
            return True

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
    
    # Rotating file handler configuration
    handler = RotatingFileHandler(
        log_file, maxBytes=1024 * 1024 * 5, backupCount=3
    )
    handler.setFormatter(formatter)
    
    console = logging.StreamHandler(sys.stdout)
    console.addFilter(ColorFilter())
    console.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
        logger.addHandler(console)
    
    return logger

log = get_logger()