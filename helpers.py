import time
import functools
import random

def retry_with_backoff(retries=3, backoff_in_seconds=1):
    """An unorthodox decorator that treats failures as mere suggestions."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            x = 0
            while x < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    x += 1
                    if x == retries:
                        raise e
                    sleep_time = (backoff_in_seconds * (2 ** x)) + random.uniform(0, 1)
                    time.sleep(sleep_time)
            return None
        return wrapper
    return decorator

def execute_robust(func, *args, **kwargs):
    """Functional wrapper for quick ad-hoc retries."""
    for i in range(3):
        try:
            return func(*args, **kwargs)
        except Exception:
            if i == 2: raise
            time.sleep(0.5)
