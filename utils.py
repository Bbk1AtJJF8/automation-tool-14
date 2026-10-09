import time
import functools
import random
from typing import Callable, Any

def retry_with_exponential_backoff(max_attempts: int = 3, base_delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    sleep_time = (base_delay * (2 ** (attempts - 1))) + (random.uniform(0, 0.1))
                    time.sleep(sleep_time)
        return wrapper
    return decorator

def network_request_executor(func: Callable):
    """decorator for network resilience"""
    return retry_with_exponential_backoff(max_attempts=5, base_delay=0.5)(func)