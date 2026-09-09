import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_FILE = Path('automation.log')

class UnconventionalFormatter(logging.Formatter):
    def format(self, record):
        base = super().format(record)
        return f'[AUTOMATION-14] {record.levelname.upper()} >>> {base}'

def get_logger(name='main'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        file_handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=1024 * 1024 * 5,
            backupCount=3
        )
        file_handler.setFormatter(UnconventionalFormatter('%(asctime)s - %(name)s - %(message)s'))
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(UnconventionalFormatter('%(message)s'))
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger