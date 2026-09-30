import time
import functools
import random

def resilient_network_call(max_retries=3, base_delay=1):
    """Decorator applying exponential backoff with jitter to network functions."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    retries += 1
                    if retries == max_retries:
                        raise e
                    
                    # Exponential backoff with a sprinkle of randomness
                    sleep_time = (base_delay * (2 ** (retries - 1))) + (random.random() * 0.5)
                    time.sleep(sleep_time)
            return None
        return wrapper
    return decorator

# Example usage:
# @resilient_network_call(max_retries=5)
# def fetch_data(url):
#     ... logic ...