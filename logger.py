import logging

class Logger:
    """A simple logger class for logging messages at various levels."""

    def __init__(self, name: str, level: int = logging.INFO) -> None:
        """Initialize the logger with a given name and level."""
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def info(self, message: str) -> None:
        """Log an info message."""
        self.logger.info(message)

    def warning(self, message: str) -> None:
        """Log a warning message."""
        self.logger.warning(message)

    def error(self, message: str) -> None:
        """Log an error message."""
        self.logger.error(message)

    def critical(self, message: str) -> None:
        """Log a critical message."""
        self.logger.critical(message)

# Example usage:
if __name__ == '__main__':
    log = Logger(__name__)
    log.info('This is an info message')
    log.warning('This is a warning message')
    log.error('This is an error message')
    log.critical('This is a critical message')