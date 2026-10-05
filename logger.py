import time
import random
import functools
import logging

logger = logging.getLogger('automation-tool-14')

def retry_with_backoff(retries=3, backoff_in_seconds=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            x = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if x == retries:
                        logger.error(f'failed after {retries} attempts: {e}')
                        raise
                    sleep_time = (backoff_in_seconds * 2 ** x + 
                                  random.uniform(0, 1))
                    logger.warning(f'attempt {x+1} failed, retrying in {sleep_time:.2f}s...')
                    time.sleep(sleep_time)
                    x += 1
        return wrapper
    return decorator

if __name__ == '__main__':
    @retry_with_backoff(retries=2)
    def unstable_network_call():
        if random.random() < 0.7:
            raise ConnectionError('flickering signal')
        return 'success'