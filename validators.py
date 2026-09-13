import time
import functools
import random

def retry_network_call(max_retries=3, backoff_factor=0.5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    if attempts == max_retries:
                        raise e
                    wait_time = backoff_factor * (2 ** (attempts - 1)) + random.uniform(0, 0.1)
                    time.sleep(wait_time)
        return wrapper
    return decorator

class NetworkValidator:
    @retry_network_call(max_retries=3)
    def ping_service(self, url):
        # Simulates network request logic
        if random.random() < 0.7:
            raise ConnectionError(f"Failed to connect to {url}")
        return True