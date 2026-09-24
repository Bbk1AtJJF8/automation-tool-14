import time
import functools
import random

def retry_operation(max_attempts=3, base_delay=1, jitter=True):
    """Decorator implementing exponential backoff for flaky network calls."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    
                    # Exponential backoff calculation
                    delay = base_delay * (2 ** (attempts - 1))
                    if jitter:
                        delay += random.uniform(0, 0.1 * delay)
                    
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

# Example usage for automation-tool-14 modules
@retry_operation(max_attempts=4)
def fetch_remote_resource(url):
    # Simulate network instability
    if random.random() < 0.7:
        raise ConnectionError(f"Failed to connect to {url}")
    return f"Payload from {url}"