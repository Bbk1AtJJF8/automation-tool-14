import logging
from logging.handlers import RotatingFileHandler
import json
import os

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

def setup_logger(log_file="app.log", max_bytes=1048576, backup_count=5):
    """
    Sets up a rotating logger that outputs logs in JSON format.
    """
    logger = logging.getLogger("automation_tool")
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
            
        handler = RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
        )
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
        
        console = logging.StreamHandler()
        console.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
        logger.addHandler(console)
        
    return logger