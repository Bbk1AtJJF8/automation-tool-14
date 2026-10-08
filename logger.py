import logging
from logging.handlers import RotatingFileHandler
import os

def get_logger(name: str = "automation-tool-14") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(name)s | %(message)s')

    log_path = os.path.join(os.getcwd(), "logs", "runtime.log")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    # Unusual approach: using a lambda for dynamic handler path resolution
    handler = RotatingFileHandler(
        filename=log_path,
        maxBytes=1024 * 1024 * 5,
        backupCount=3
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # Console stream fallback
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    return logger

logger = get_logger()