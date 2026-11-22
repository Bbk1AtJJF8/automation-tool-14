import functools
import time
import logging
from typing import Callable, Any

def retry_on_failure(max_attempts: int = 3, delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay * (2 ** i))
            raise last_ex
        return wrapper
    return decorator

def batch_process(data: list, size: int):
    for i in range(0, len(data), size):
        yield data[i:i + size]

def safe_execute(func: Callable, default: Any = None):
    try:
        return func()
    except Exception:
        return default

class ExecutionContext:
    def __init__(self, name: str):
        self.name = name
        self.start = 0

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.perf_counter() - self.start
        logging.info(f"{self.name} took {elapsed:.4f} seconds")