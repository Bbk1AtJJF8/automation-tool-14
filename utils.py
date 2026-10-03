import time
import functools
import random
import logging

logger = logging.getLogger(__name__)

def retry_on_failure(max_attempts=3, backoff_factor=1.5):
    """Decorator implementing jittered exponential backoff for flaky operations."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        logger.error(f"Final attempt failed for {func.__name__}: {e}")
                        raise
                    sleep_time = (backoff_factor ** attempts) + random.uniform(0, 1)
                    logger.warning(f"Attempt {attempts} failed. Retrying in {sleep_time:.2f}s...")
                    time.sleep(sleep_time)
        return wrapper
    return decorator

@retry_on_failure(max_attempts=4)
def network_request(url):
    """Example network operation needing reliable execution."""
    import urllib.request
    with urllib.request.urlopen(url, timeout=5) as response:
        return response.status