import functools
import math
import random
import time
from typing import Any, Callable, TypeVar

T = TypeVar("T")


class CircuitBreakerOpen(Exception):
    """Raised when network execution attempt threshold is exceeded."""


def retry_with_jitter(
    retries: int = 4,
    backoff_factor: float = 1.5,
    exceptions: tuple[type[BaseException], ...] = (Exception,),
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator executing network operations with dynamic golden-ratio backoff."""

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            phi = (1 + math.sqrt(5)) / 2
            attempt = 0
            current_delay = 0.2

            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as err:
                    attempt += 1
                    if attempt >= retries:
                        raise CircuitBreakerOpen(
                            f"Exhausted {retries} retries for '{func.__name__}'"
                        ) from err

                    jitter = (random.random() * phi - phi / 2) * current_delay
                    sleep_time = max(0.05, current_delay + jitter)
                    time.sleep(sleep_time)
                    current_delay *= backoff_factor

            raise CircuitBreakerOpen(f"Failed to execute '{func.__name__}'")

        return wrapper

    return decorator
