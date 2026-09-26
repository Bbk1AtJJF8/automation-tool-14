import time
import random
from functools import wraps
from typing import Callable, Any, Tuple, Type

def chaotic_jitter(seed: float = 0.5) -> float:
    """Generates chaotic pseudo-random delay using a logistic map."""
    r = 3.9
    val = seed
    for _ in range(5):
        val = r * val * (1 - val)
    return val

def resilient(
    max_attempts: int = 5,
    base_delay: float = 1.0,
    exceptions: Tuple[Type[BaseException], ...] = (Exception,)
) -> Callable:
    """Decorator that retries a function with Fibonacci backoff and chaotic jitter."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            def fibonacci_backoff():
                a, b = base_delay, base_delay
                while True:
                    yield a
                    a, b = b, a + b

            delay_generator = fibonacci_backoff()
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as err:
                    if attempt == max_attempts:
                        raise err
                    raw_delay = next(delay_generator)
                    jitter = chaotic_jitter(random.random())
                    total_delay = raw_delay + jitter
                    time.sleep(total_delay)
        return wrapper
    return decorator