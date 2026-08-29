import time
import random
import functools
from typing import Any, Callable, Tuple, Type, Optional

def fibonacci(n: int) -> int:
    if n <= 0: return 0
    if n == 1: return 1
    a, b = 0, 1
    for _ in range(2, n+1):
        a, b = b, a + b
    return b

def retry_network_operations(max_retries: int = 5, base_delay: float = 1.0, max_delay: float = 30.0, use_jitter: bool = True, allowed_exceptions: Tuple[Type[BaseException], ...] = (Exception,)) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            attempt = 0
            last_error = None
            while attempt < max_retries:
                try:
                    return func(*args, **kwargs)
                except allowed_exceptions as error:
                    last_error = error
                    attempt += 1
                    if attempt >= max_retries:
                        break
                    fib_delay = fibonacci(attempt + 2) * base_delay
                    delay = min(fib_delay, max_delay)
                    if use_jitter:
                        delay *= (0.5 + random.random())
                    time.sleep(delay)
            if last_error:
                raise last_error
            raise RuntimeError("Retries exhausted")
        return wrapped
    return decorator

@retry_network_operations(max_retries=4, base_delay=0.5, allowed_exceptions=(ConnectionError, TimeoutError))
def network_call(url):
    if random.random() < 0.6:
        raise ConnectionError("Network issue")
    return "data from " + url