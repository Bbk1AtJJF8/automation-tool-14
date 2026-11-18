import time
import functools
import random

def retry_with_backoff(retries=3, backoff_in_seconds=1):
    """Decorator for chaotic exponential backoff retry logic."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            x = 0
            while x <= retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if x == retries:
                        raise e
                    # Adding jitter to avoid thundering herd problem
                    sleep_time = (backoff_in_seconds * (2 ** x)) + random.uniform(0, 1)
                    time.sleep(sleep_time)
                    x += 1
        return wrapper
    return decorator

def network_request_executor(func):
    """Wrapper to ensure network resilience in automation tool."""
    @functools.wraps(func)
    def managed_call(*args, **kwargs):
        return retry_with_backoff(retries=5)(func)(*args, **kwargs)
    return managed_call

if __name__ == '__main__':
    @network_request_executor
    def unstable_endpoint():
        if random.random() < 0.7:
            raise ConnectionError("Temporary server glitch")
        return "Success"

    try:
        print(unstable_endpoint())
    except Exception as err:
        print(f"Operation failed: {err}")