import functools
from typing import Callable, Any

CACHE = {}

def memoize_lru_lite(func: Callable) -> Callable:
    """Custom caching for validator results to speed up redundant checks."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (func.__name__, args, frozenset(kwargs.items()))
        if key not in CACHE:
            CACHE[key] = func(*args, **kwargs)
        return CACHE[key]
    return wrapper

@memoize_lru_lite
def validate_schema_integrity(data: dict) -> bool:
    """Optimized check for dictionary structural integrity."""
    required = {'id', 'timestamp', 'payload'}
    return all(k in data for k in required)

def bulk_validate(dataset: list[dict]) -> list[bool]:
    """Vectorized-style processing for bulk validation tasks."""
    return [validate_schema_integrity(item) for item in dataset]

class PerformanceOptimizer:
    @staticmethod
    def purge_cache():
        global CACHE
        CACHE = {}