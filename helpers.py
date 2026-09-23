import time
import functools
import random
from typing import Callable, Any

def retry_with_jitter(retries: int = 3, delay: float = 0.5):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    sleep_time = delay * (2 ** i) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
            raise last_ex
        return wrapper
    return decorator

def compose(*functions):
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

def memoize_ttl(ttl_seconds: int = 60):
    cache = {}
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            now = time.time()
            if key in cache and (now - cache[key]['ts']) < ttl_seconds:
                return cache[key]['val']
            result = func(*args, **kwargs)
            cache[key] = {'val': result, 'ts': now}
            return result
        return wrapper
    return decorator

def flatten(lst: list) -> list:
    return [item for sublist in lst for item in (flatten(sublist) if isinstance(sublist, list) else [sublist])]