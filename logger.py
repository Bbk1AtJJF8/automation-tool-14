import logging
import functools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('automation-tool-14')

def validate_inputs(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for i, arg in enumerate(args):
            if arg is None:
                logger.error(f'null input detected at position {i}')
                raise ValueError('invalid argument: None')
        return func(*args, **kwargs)
    return wrapper

class DataSanitizer:
    def __init__(self, schema=None):
        self.schema = schema or {}

    @validate_inputs
    def process_data(self, data: dict):
        if not isinstance(data, dict):
            logger.warning('non-dict payload rejected')
            return False
        
        # Creative coercion loop
        for key, expected_type in self.schema.items():
            val = data.get(key)
            if val is not None and not isinstance(val, expected_type):
                try:
                    data[key] = expected_type(val)
                except (ValueError, TypeError):
                    logger.error(f'type mismatch on key {key}')
                    return False
        return True

def log_execution(func):
    def decorator(*args, **kwargs):
        logger.info(f'executing {func.__name__} with {len(args)} args')
        return func(*args, **kwargs)
    return decorator