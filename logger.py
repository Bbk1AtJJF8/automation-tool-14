import logging
from logging.handlers import RotatingFileHandler
import os

def get_automation_logger(name: str = 'automation-tool-14') -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        handler = RotatingFileHandler(
            os.path.join(log_dir, f'{name}.log'),
            maxBytes=1024 * 1024 * 5,
            backupCount=3
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
        
    return logger

if __name__ == '__main__':
    log = get_automation_logger()
    log.info('logger initialization sequence complete')