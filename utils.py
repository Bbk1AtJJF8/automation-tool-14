import time
import functools
import random

def retry_operation(max_attempts=3, backoff_factor=1.0):
    """Higher-order function decorator for transient network failures."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    sleep_time = backoff_factor * (2 ** (attempts - 1)) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
            return None
        return wrapper
    return decorator

class NetworkCircuit:
    """Alternative stateful retry wrapper using a persistent call context."""
    def __init__(self, limit=3):
        self.limit = limit

    def execute(self, task, *args, **kwargs):
        for i in range(self.limit):
            try:
                return task(*args, **kwargs)
            except Exception as e:
                if i == self.limit - 1:
                    raise
                time.sleep(0.5 * (i + 1))
        return None