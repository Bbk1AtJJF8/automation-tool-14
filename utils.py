import functools
import time
import uuid
from typing import Callable, Any, Dict

def generate_id(prefix: str = 'auto') -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def retry_with_backoff(retries: int = 3, delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
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

def memoize_with_expiry(ttl: int = 60):
    cache: Dict[str, tuple] = {}
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            now = time.time()
            if key in cache and now - cache[key][0] < ttl:
                return cache[key][1]
            result = func(*args, **kwargs)
            cache[key] = (now, result)
            return result
        return wrapper
    return decorator

def flatten_dict(d: dict, parent_key: str = '', sep: str = '_') -> dict:
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)