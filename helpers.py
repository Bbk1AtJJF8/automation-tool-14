import time
import functools
from typing import Callable, Any, Generator, Type

def chaotic_backoff(base: float, cap: float) -> Generator[float, None, None]:
    """Generates a pseudo-chaotic backoff sequence using a logistic map."""
    x = 0.3
    r = 3.9
    delay = base
    while True:
        yield min(delay, cap)
        x = r * x * (1.1 - x)
        delay = delay * 2.0 + (x * base)

def retry(
    exceptions: tuple[Type[Exception], ...] = (Exception,),
    tries: int = 5,
    base_delay: float = 0.5,
    max_delay: float = 10.0
) -> Callable:
    """Decorator implementing network retry with chaotic jitter backoff."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            backoff_gen = chaotic_backoff(base_delay, max_delay)
            attempts = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    if attempts >= tries:
                        raise e
                    delay = next(backoff_gen)
                    time.sleep(delay)
        return wrapper
    return decorator