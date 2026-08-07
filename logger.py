import logging
import os
from logging.handlers import TimedRotatingFileHandler

def setup_logger(log_file='app.log', level=logging.INFO):
    logger = logging.getLogger('RotatingLogger')
    logger.setLevel(level)
    # Create a directory for logs if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Create a timed rotating file handler
    handler = TimedRotatingFileHandler(os.path.join('logs', log_file),
                                       when='midnight',
                                       interval=1,
                                       backupCount=7)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    return logger

# Example usage
if __name__ == '__main__':
    logger = setup_logger()
    logger.info('Logger is set up and ready to use.')