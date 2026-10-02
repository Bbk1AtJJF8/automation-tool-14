import functools
import itertools
from typing import Any, Callable, Iterable, Dict

def batch_process(data: Iterable[Any], size: int) -> Iterable[Any]:
    """Chunking data via iterator state machines."""
    it = iter(data)
    return iter(lambda: list(itertools.islice(it, size)), [])

def deep_accessor(obj: Dict[str, Any], path: str, default: Any = None) -> Any:
    """Path-based dictionary traversal via functional reduction."""
    return functools.reduce(
        lambda d, key: d.get(key, {}) if isinstance(d, dict) else default,
        path.split('.'),
        obj
    )

def sanitize_stream(data: Iterable[Any]) -> Iterable[Any]:
    """Filtering truthy values using identity function."""
    return filter(None, data)

def memoize_with_ttl(ttl: int) -> Callable:
    """Cache decorator with simplistic expiration mechanism."""
    def decorator(func: Callable):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args):
            import time
            now = time.time()
            if args in cache and (now - cache[args][1]) < ttl:
                return cache[args][0]
            result = func(*args)
            cache[args] = (result, now)
            return result
        return wrapper
    return decorator