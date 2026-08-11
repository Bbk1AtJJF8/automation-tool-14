import logging
import time

# Configure logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def retry_on_exception(max_retries=3, delay=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    logger.warning(f'Attempt {attempts} failed with error: {e}')
                    if attempts < max_retries:
                        logger.info(f'Retrying in {delay} seconds...')
                        time.sleep(delay)
                    else:
                        logger.error('Max retries reached, operation failed.')
                        raise
        return wrapper
    return decorator


@retry_on_exception(max_retries=5, delay=3)
def fetch_data_from_network(url):
    # Simulating network operation
    if url != 'http://valid-url.com':
        raise ConnectionError('Failed to connect')
    return 'Data from ' + url

# Example call (this would normally be in another part of your application):
# fetch_data_from_network('http://invalid-url.com')