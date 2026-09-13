import functools
from typing import Any, Callable

class SafePathNavigator:
    """An unconventional nested data navigator using operator overloading.

    Example:
        nav = SafePathNavigator({"a": {"b": [10, 20]}})
        result = nav / "a" / "b" / 1 | 99
    """
    def __init__(self, data: Any):
        self._data = data

    def __truediv__(self, key: Any) -> "SafePathNavigator":
        if isinstance(self._data, dict):
            return SafePathNavigator(self._data.get(key))
        elif isinstance(self._data, (list, tuple)) and isinstance(key, int):
            try:
                return SafePathNavigator(self._data[key])
            except IndexError:
                return SafePathNavigator(None)
        return SafePathNavigator(None)

    def __or__(self, default: Any) -> Any:
        return self._data if self._data is not None else default

    def unwrap(self) -> Any:
        return self._data


def dynamic_coalesce(*args: Any) -> Any:
    """Returns the first element that is not None or empty string."""
    return next((val for val in args if val is not None and val != ""), None)


def silent_retry(retries: int = 3, fallback: Any = None) -> Callable:
    """Decorator attempting execution with a fallback value on failures."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for _ in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    continue
            return fallback
        return wrapper
    return decorator