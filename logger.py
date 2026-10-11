import logging
from logging.handlers import RotatingFileHandler
import os

def get_automaton_logger(name='automation-tool-14'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if logger.handlers:
        return logger

    log_path = os.path.join(os.getcwd(), 'logs', f'{name}.log')
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = RotatingFileHandler(
        log_path, 
        maxBytes=1048576, 
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Instantiate for global use via simple injection
logger = get_automaton_logger()