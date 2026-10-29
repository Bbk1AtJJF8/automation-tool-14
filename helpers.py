import time
import random
import functools
from typing import Callable, Any, Tuple, Type, Generator

class RetryExhaustedError(Exception):
    """Raised when network execution exhausts allowed retry limit."""
    pass

def _jittered_backoff(base_delay: float, factor: float, max_delay: float) -> Generator[float, None, None]:
    """Generator producing exponential backoff intervals with random jitter."""
    delay = base_delay
    while True:
        jitter = random.uniform(0.85, 1.15)
        yield min(delay * jitter, max_delay)
        delay *= factor

def network_retry(
    retries: int = 4,
    base_delay: float = 0.2,
    backoff_factor: float = 2.0,
    max_delay: float = 5.0,
    retryable_exceptions: Tuple[Type[Exception], ...] = (TimeoutError, ConnectionError, OSError)
):
    """Decorator applying dynamic jittered backoff retry strategies to callables."""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            backoff_stream = _jittered_backoff(base_delay, backoff_factor, max_delay)
            last_exc = None
            
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except retryable_exceptions as exc:
                    last_exc = exc
                    if attempt == retries:
                        break
                    wait_time = next(backoff_stream)
                    time.sleep(wait_time)
            
            raise RetryExhaustedError(
                f"Target '{func.__name__}' failed after {retries} retries. Cause: {last_exc}"
            ) from last_exc
        return wrapper
    return decorator