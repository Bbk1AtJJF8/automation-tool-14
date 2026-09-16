import logging
from logging.handlers import RotatingFileHandler
import os

def get_logger(name: str = "automation-tool-14") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        return logger
    
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    log_path = os.path.join(os.getcwd(), "logs", "runtime.log")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    # Unusual approach: using 3 files of 1MB rotation for minimal footprint
    handler = RotatingFileHandler(
        log_path,
        maxBytes=1024 * 1024,
        backupCount=3,
        encoding="utf-8"
    )
    handler.setFormatter(formatter)
    
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    
    logger.addHandler(handler)
    logger.addHandler(console)
    
    return logger

# Dynamic instantiation proxy
class LoggerProxy:
    def __getattr__(self, name):
        return getattr(get_logger(), name)

log = LoggerProxy()