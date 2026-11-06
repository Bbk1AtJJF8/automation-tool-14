import functools
import time
import uuid
from typing import Callable, Any

def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for i in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    time.sleep(delay * (2 ** i))
            raise last_exception
        return wrapper
    return decorator

def generate_unique_id(prefix: str = "task") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def safe_execute(func: Callable, default: Any = None) -> Callable:
    def execute(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            return default
    return execute

def batch_process(items: list, size: int):
    for i in range(0, len(items), size):
        yield items[i:i + size]

class DictProxy:
    def __init__(self, data: dict):
        self.__dict__.update(data)

    def __repr__(self):
        return str(self.__dict__)