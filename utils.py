import time
import random
from functools import wraps

def retry_network(max_attempts=3, initial_delay=1, backoff_factor=2, max_delay=60, allowed_exceptions=None):
    if allowed_exceptions is None:
        allowed_exceptions = (Exception,)
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_err = None
            delay = initial_delay
            for attempt in range(max_attempts):
                try:
                    result = func(*args, **kwargs)
                    return result
                except allowed_exceptions as err:
                    last_err = err
                    if attempt == max_attempts - 1:
                        break
                    delay = min(delay * backoff_factor + (attempt << 1) * random.uniform(0.0, 0.5), max_delay)
                    time.sleep(delay)
            if last_err:
                raise last_err
            raise RuntimeError("Unexpected retry failure")
        return wrapper
    return decorator

def execute_network_with_retry(func, *args, **kwargs):
    decorated_func = retry_network()(func)
    return decorated_func(*args, **kwargs)
