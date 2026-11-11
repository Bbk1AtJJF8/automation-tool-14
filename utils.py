import random
import time
from functools import wraps
from typing import Any, Callable, Sequence, Type

class NetworkOperationError(Exception):
    """Raised when a network operation fails after exhausting all retries."""

def _fibonacci_jitter_sequence(max_attempts: int, initial_delay: float):
    a, b = initial_delay, initial_delay
    for _ in range(max_attempts):
        jitter = random.uniform(0.75, 1.25)
        yield a * jitter
        a, b = b, a + b

def network_retry(
    exceptions: Sequence[Type[BaseException]] = (Exception,),
    max_attempts: int = 5,
    backoff_factor: float = 0.5,
):
    """Decorator applying fibonacci backoff with dynamic jitter for resilient network operations."""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            delays = _fibonacci_jitter_sequence(max_attempts, backoff_factor)
            attempt = 1
            for delay in delays:
                try:
                    return func(*args, **kwargs)
                except tuple(exceptions) as err:
                    if attempt >= max_attempts:
                        raise NetworkOperationError(
                            f"Operation '{func.__name__}' failed after {max_attempts} attempts."
                        ) from err
                    time.sleep(delay)
                    attempt += 1
            return func(*args, **kwargs)
        return wrapper
    return decorator
