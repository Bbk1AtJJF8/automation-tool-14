import functools
import time
import logging
from typing import Callable, Any

def retry_operation(attempts: int = 3, delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay * (2 ** i))
            raise last_ex
        return wrapper
    return decorator

def sanitize_input(data: dict) -> dict:
    return {k: str(v).strip() for k, v in data.items() if v is not None}

class ExecutionPipeline:
    def __init__(self):
        self.steps = []

    def pipe(self, func: Callable):
        self.steps.append(func)
        return self

    def execute(self, value: Any):
        result = value
        for step in self.steps:
            result = step(result)
        return result

def setup_logging(name: str):
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger