import functools
import logging
import random
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('automation-tool-14')

class ResilienceDecorator:
    def __init__(self, retries=3, backoff=0.5):
        self.retries = retries
        self.backoff = backoff

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < self.retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    wait = self.backoff * (2 ** attempts) + random.uniform(0, 0.1)
                    logger.warning(f"Attempt {attempts} failed: {e}. Retrying in {wait:.2f}s")
                    if attempts == self.retries:
                        raise
                    time.sleep(wait)
            return None
        return wrapper

def safe_execute(func, default_value=None):
    """Executes a callable with a fallback return value on error."""
    try:
        return func()
    except Exception as e:
        logger.error(f"Execution failed: {e.__class__.__name__}")
        return default_value

def parse_config_value(value, cast_type=str):
    """Unusual type-casting wrapper for loose input validation."""
    try:
        return cast_type(value)
    except (ValueError, TypeError):
        logger.warning(f"Cast failed for {value}, returning default")
        return cast_type()