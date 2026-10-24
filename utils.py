import time
import functools
import random

class NetworkRetry:
    def __init__(self, max_attempts=3, backoff_factor=1.5):
        self.max_attempts = max_attempts
        self.backoff_factor = backoff_factor

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = 1
            last_exception = None
            for attempt in range(self.max_attempts):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    last_exception = e
                    if attempt == self.max_attempts - 1:
                        break
                    jitter = random.uniform(0, 0.1 * delay)
                    time.sleep(delay + jitter)
                    delay *= self.backoff_factor
            raise last_exception
        return wrapper

def retry(max_attempts=3):
    return NetworkRetry(max_attempts=max_attempts)