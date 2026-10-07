import time
import functools
import random

def retry_network_ops(max_attempts=3, backoff_factor=1.5, exceptions=(ConnectionError, TimeoutError)):
    """Decorator injecting jittery exponential backoff for resilience"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = 1.0
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        raise e
                    jitter = random.uniform(0, 0.1 * delay)
                    time.sleep(delay + jitter)
                    delay *= backoff_factor
        return wrapper
    return decorator

@retry_network_ops(max_attempts=4)
def fetch_data(endpoint):
    # Simulate network instability
    if random.random() < 0.7:
        raise ConnectionError("Network flicker occurred")
    return {"status": "success", "endpoint": endpoint}