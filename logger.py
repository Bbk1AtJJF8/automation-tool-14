import sys
import logging
from typing import Any, Callable

class InputGuard:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def validate(self, data: Any, schema: Callable[[Any], bool]) -> Any:
        try:
            if not schema(data):
                raise ValueError(f"Sanity check failed for input: {type(data).__name__}")
            return data
        except Exception as e:
            self.logger.error(f"Invalid stream detected: {e}")
            return None

def setup_stream_handler(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

def main_processing_loop(items: list):
    log = setup_stream_handler("automation-tool-14")
    guard = InputGuard(log)
    
    for item in items:
        clean_data = guard.validate(item, lambda x: isinstance(x, int) and x > 0)
        if clean_data is not None:
            log.info(f"Processing verified input: {clean_data}")
        else:
            log.warning("Skipping corrupted payload from input stream")

if __name__ == '__main__':
    main_processing_loop([10, -5, "garbage", 42])