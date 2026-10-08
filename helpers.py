import json
import time
from functools import wraps
from typing import Callable, Any

def retry_on_failure(retries: int = 3, delay: float = 1.0):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay * (2 ** i))
            raise last_ex
        return wrapper
    return decorator

def slugify_string(text: str) -> str:
    return "-".join(text.lower().split()).encode("ascii", "ignore").decode()

def safe_json_load(file_path: str, default: Any = None) -> Any:
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

def batch_process(iterable: list, size: int):
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]

class ContextTimer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self
    def __exit__(self, *args):
        self.elapsed = time.perf_counter() - self.start