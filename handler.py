import time
import functools
import logging
from typing import Callable, Any

def retry_on_failure(retries: int = 3, delay: float = 1.0):
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

def batch_process(items: list, size: int):
    return [items[i:i + size] for i in range(0, len(items), size)]

def memoize_with_expiry(ttl: int = 60):
    cache = {}
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args):
            key = str(args)
            now = time.time()
            if key in cache and now - cache[key]["ts"] < ttl:
                return cache[key]["val"]
            result = func(*args)
            cache[key] = {"val": result, "ts": now}
            return result
        return wrapper
    return decorator

def silent_executor(func: Callable, *args, **kwargs) -> Any:
    try:
        return func(*args, **kwargs)
    except Exception:
        return None