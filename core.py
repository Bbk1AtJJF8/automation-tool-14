import functools
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('automation-tool-14')

def resilient_wrapper(retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except (ValueError, TypeError, ConnectionError) as e:
                    last_ex = e
                    logger.warning(f'Edge case detected in {func.__name__}: {e}. Retrying {attempt+1}/{retries}')
                    time.sleep(delay * (2 ** attempt))
            logger.error(f'Critical failure in {func.__name__} after {retries} attempts.')
            raise last_ex
        return wrapper
    return decorator

@resilient_wrapper(retries=2)
def execute_task(payload):
    if not isinstance(payload, dict):
        raise ValueError('payload must be a dict')
    if 'action' not in payload:
        raise TypeError('missing action key')
    return f'Processed: {payload['action']}'

def run_pipeline(data_stream):
    results = []
    for item in data_stream:
        try:
            results.append(execute_task(item))
        except Exception as e:
            results.append({'error': str(e), 'status': 'failed'})
    return results