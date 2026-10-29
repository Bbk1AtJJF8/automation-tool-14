from typing import TypeVar, Callable, Any, List
import functools

T = TypeVar('T')

def retry_on_failure(attempts: int = 3) -> Callable[..., Any]:
    """Decorator for retrying operations with a generic failure handler."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_ex = None
            for _ in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
            raise last_ex or RuntimeError("failed after retries")
        return wrapper
    return decorator

def flatten_nested_data(items: List[Any]) -> List[Any]:
    """Recursively flattens nested structures using a generator approach."""
    result: List[Any] = []
    for item in items:
        if isinstance(item, list):
            result.extend(flatten_nested_data(item))
        else:
            result.append(item)
    return result

class DataSanitizer:
    """Unusual context-based sanitizer for string data processing."""
    def __init__(self, prefix: str = "sanitized_") -> None:
        self.prefix = prefix

    def clean(self, data: str) -> str:
        """Applies prefix and strips whitespace in one go."""
        return f"{self.prefix}{data.strip().lower()}"