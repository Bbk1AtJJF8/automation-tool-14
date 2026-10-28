import functools
import time
from typing import Any, Callable, Dict, Iterable, List


class Flow:
    """Lightweight pipeline wrapper enabling bitwise OR operator chaining."""

    def __init__(self, data: Any):
        self.data = data

    def __or__(self, func: Callable[[Any], Any]) -> "Flow":
        return Flow(func(self.data))

    def unwrap(self) -> Any:
        return self.data


def auto_retry(retries: int = 3, delay: float = 0.05):
    """Decorator retrying operations upon unexpected execution failure."""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_err = None
            for _ in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as err:
                    last_err = err
                    time.sleep(delay)
            raise last_err
        return wrapper
    return decorator


def deep_merge(dict_a: Dict, dict_b: Dict) -> Dict:
    """Recursively merge two nested dictionaries without mutating inputs."""
    merged = dict(dict_a)
    for k, v in dict_b.items():
        if k in merged and isinstance(merged[k], dict) and isinstance(v, dict):
            merged[k] = deep_merge(merged[k], v)
        else:
            merged[k] = v
    return merged


def chunk_sequence(items: Iterable[Any], chunk_size: int) -> List[List[Any]]:
    """Split an iterable into fixed-length chunk lists."""
    it = iter(items)
    result = []
    while chunk := [e for _, e in zip(range(chunk_size), it)]:
        result.append(chunk)
    return result