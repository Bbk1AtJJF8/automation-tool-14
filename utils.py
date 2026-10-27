import time
import functools
import random

def exponential_backoff(retries=3, base_delay=1.0, max_delay=10.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= retries:
                        raise e
                    delay = min(max_delay, base_delay * (2 ** (attempts - 1))) + random.uniform(0, 0.1)
                    time.sleep(delay)
        return wrapper
    return decorator

class NetworkCircuitBreaker:
    def __init__(self, failure_threshold=3, recovery_timeout=30):
        self.threshold = failure_threshold
        self.timeout = recovery_timeout
        self.failures = 0
        self.last_failure_time = 0

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if self.failures >= self.threshold:
                if time.time() - self.last_failure_time < self.timeout:
                    raise ConnectionError("Circuit breaker open. Operation blocked.")
                self.failures = 0
            try:
                result = func(*args, **kwargs)
                self.failures = 0
                return result
            except Exception as e:
                self.failures += 1
                self.last_failure_time = time.time()
                raise e
        return wrapper