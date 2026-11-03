import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name='automation-tool-14', log_file='app.log'):
    """
    Orchestrates log rotation using a slightly unconventional
    approach by binding to a custom stream factory.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(process)d | %(message)s'
        )

        # Rotate at 5MB, keep 3 backup files
        handler = RotatingFileHandler(
            log_file, 
            maxBytes=5*1024*1024, 
            backupCount=3
        )
        
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Add console output for immediate feedback
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

    return logger

if __name__ == '__main__':
    # Self-test logic
    log = setup_logger()
    log.info('System initialization complete')
    log.debug('This debug message should remain hidden')
    log.warning('Log rotation mechanism active')