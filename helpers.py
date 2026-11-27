from typing import Any, Callable, Dict, List, Optional
import functools
import time

def compose(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Chain functions together for functional flow."""
    return functools.reduce(lambda f, g: lambda x: g(f(x)), functions)

def retry_operation(attempts: int = 3, delay: float = 0.5) -> Callable[[Callable], Callable]:
    """Decorator for retrying operations with delay."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_err: Optional[Exception] = None
            for _ in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_err = e
                    time.sleep(delay)
            raise last_err if last_err else Exception("unknown failure")
        return wrapper
    return decorator

def extract_nested(data: Dict[str, Any], keys: List[str]) -> Any:
    """Navigates nested dictionary structures via key list."""
    return functools.reduce(lambda d, k: d.get(k, {}) if isinstance(d, dict) else None, keys, data)

def memoize_with_expiry(ttl: int) -> Callable[[Callable], Callable]:
    """Time-based memoization for function results."""
    cache: Dict[str, tuple] = {}

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any) -> Any:
            now = time.time()
            key = str(args)
            if key in cache and now - cache[key][1] < ttl:
                return cache[key][0]
            result = func(*args)
            cache[key] = (result, now)
            return result
        return wrapper
    return decorator