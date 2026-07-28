import logging

class Logger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_info(self, message):
        if self.validate_message(message):
            self.logger.info(message)

    def log_warning(self, message):
        if self.validate_message(message):
            self.logger.warning(message)

    def log_error(self, message):
        if self.validate_message(message):
            self.logger.error(message)

    def validate_message(self, message):
        if not isinstance(message, str):
            self.logger.error('Invalid message type. Must be string.')
            return False
        if len(message) == 0:
            self.logger.error('Message cannot be empty.')
            return False
        return True

# Example usage:
if __name__ == '__main__':
    logger = Logger('MyApp')
    logger.log_info('This is an info message.')
    logger.log_warning('This is a warning message.')
    logger.log_error('This is an error message.')