import logging
import os
from logging.handlers import RotatingFileHandler

def get_logger(name: str = 'automation-tool-14') -> logging.Logger:
    log_path = os.path.join(os.getcwd(), 'logs', f'{name}.log')
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(module)s]: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        rotator = RotatingFileHandler(
            log_path, 
            maxBytes=5 * 1024 * 1024, 
            backupCount=3
        )
        rotator.setFormatter(formatter)
        logger.addHandler(rotator)
        
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
        
    return logger

if __name__ == '__main__':
    log = get_logger()
    log.info('System initialization sequence triggered')