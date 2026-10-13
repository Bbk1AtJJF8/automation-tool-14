from typing import Any, Callable, Dict, List, Optional
import functools
import time

def compose_handlers(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Chain multiple callables into a single pipeline operation."""
    def pipeline(data: Any) -> Any:
        return functools.reduce(lambda v, f: f(v), functions, data)
    return pipeline

def retry_execution(retries: int = 3, delay: float = 0.5) -> Callable[[Callable], Callable]:
    """Decorator for resilient execution with exponential backoff."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_err: Optional[Exception] = None
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_err = e
                    time.sleep(delay * (2 ** i))
            raise last_err if last_err else RuntimeError("Retry failed")
        return wrapper
    return decorator

def flatten_config(data: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
    """Recursive flattening of nested dictionary structures."""
    items: List[tuple] = []
    for k, v in data.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_config(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)