import time
from typing import Any, Callable, Dict, List, Optional


class AutoPipe:
    """A fluent pipeline wrapper enabling bitwise OR (|) syntax for transformations."""
    def __init__(self, value: Any):
        self.value = value

    def __or__(self, func: Callable[[Any], Any]) -> 'AutoPipe':
        if callable(func):
            return AutoPipe(func(self.value))
        return self

    def unwrap(self) -> Any:
        return self.value


def deep_get(data: Dict[str, Any], path: str, default: Any = None) -> Any:
    """Extract nested dictionary values using dot notation paths."""
    keys = path.split('.')
    curr = data
    for k in keys:
        if isinstance(curr, dict) and k in curr:
            curr = curr[k]
        else:
            return default
    return curr


def retry_exec(func: Callable[[], Any], retries: int = 3, delay: float = 0.5) -> Any:
    """Executes a parameterless callable with exponential backoff on failure."""
    last_exc: Optional[Exception] = None
    for attempt in range(retries):
        try:
            return func()
        except Exception as e:
            last_exc = e
            time.sleep(delay * (2 ** attempt))
    if last_exc:
        raise last_exc
    raise RuntimeError("Execution failed without specific exception")


def batch_process(items: List[Any], size: int) -> List[List[Any]]:
    """Splits a list into chunks of the specified size."""
    if size <= 0:
        raise ValueError("Batch size must be greater than zero")
    return [items[i:i + size] for i in range(0, len(items), size)]
