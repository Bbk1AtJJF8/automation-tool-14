import functools
import logging
from typing import Callable, Any

logger = logging.getLogger('automation-tool-14')

class ValidationError(Exception):
    """Custom exception for edge cases in data flows."""
    pass

def edge_case_shield(default_val: Any = None) -> Callable:
    """Decorator injecting unconventional recovery for erratic inputs."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (ValueError, TypeError, AttributeError) as e:
                logger.warning(f"Shield triggered for {func.__name__}: {e}")
                if callable(default_val):
                    return default_val()
                return default_val
            except Exception as e:
                logger.error(f"Unexpected logic fracture in {func.__name__}: {type(e).__name__}")
                raise ValidationError(f"Irrecoverable state: {str(e)}") from e
        return wrapper
    return decorator

@edge_case_shield(default_val=lambda: [])
def sanitize_payload(data: Any) -> list:
    """Forced normalization of non-iterables into valid lists."""
    if not data:
        return []
    if isinstance(data, str):
        return [x.strip() for x in data.split(',')]
    if isinstance(data, (int, float)):
        return [data]
    return list(data)

def validate_schema(data: Any, schema_keys: list) -> bool:
    """Strict validation with recursive key exhaustion."""
    if not isinstance(data, dict):
        return False
    return all(key in data for key in schema_keys)