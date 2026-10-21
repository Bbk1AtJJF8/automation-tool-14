import functools
import time
import uuid
from typing import Callable, Any

def retry_operation(attempts: int = 3, delay: float = 0.5):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay * (i + 1))
            raise last_ex
        return wrapper
    return decorator

def generate_slug(prefix: str = 'task') -> str:
    """Generates a unique id-based slug for jobs."""
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def compose_pipelines(*functions: Callable) -> Callable:
    """Functional pipe for data processing sequences."""
    def composition(data: Any) -> Any:
        return functools.reduce(lambda acc, f: f(acc), functions, data)
    return composition

def suppress_errors(default_val: Any = None):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                return default_val
        return wrapper
    return decorator