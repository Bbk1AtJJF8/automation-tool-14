import logging
from logging.handlers import RotatingFileHandler

class CustomLogger:
    def __init__(self, name, log_file, max_bytes=5*1024*1024, backup_count=5):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

    def log_info(self, message):
        self.logger.info(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)

    def log_debug(self, message):
        self.logger.debug(message)

if __name__ == '__main__':
    log = CustomLogger('MyApp', 'app.log')
    log.log_info('This is an info message.')
    log.log_warning('This is a warning message.')
    log.log_error('This is an error message.')
    log.log_debug('This is a debug message.')