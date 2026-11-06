import time
import functools
import logging

logger = logging.getLogger(__name__)

def resilient_network_call(max_retries=3, delay=1.5, backoff=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError, OSError) as e:
                    if attempt == max_retries - 1:
                        logger.error(f'final attempt failed for {func.__name__}')
                        raise
                    logger.warning(f'retry {attempt + 1}/{max_retries} after error: {e}')
                    time.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator

class ExponentialBackoffIterator:
    def __init__(self, start=1, factor=2, limit=60):
        self.current = start
        self.factor = factor
        self.limit = limit

    def __iter__(self):
        return self

    def __next__(self):
        val = self.current
        self.current = min(self.current * self.factor, self.limit)
        return val