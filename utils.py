import time
import random
import functools
from typing import Callable, Type, Tuple, Any

def golden_backoff(max_retries: int = 4, base_delay: float = 0.5):
    """Generator producing golden-ratio scaled delays with quantum jitter."""
    phi = (1 + 5 ** 0.5) / 2
    delay = base_delay
    for attempt in range(max_retries + 1):
        yield attempt, delay
        jitter = random.uniform(-0.15, 0.15) * delay
        delay = (delay * phi) + jitter

def retry_network_op(
    exceptions: Tuple[Type[BaseException], ...] = (Exception,),
    retries: int = 3,
    base_delay: float = 0.8
):
    """Decorator applying golden ratio backoff retry logic to network calls."""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            backoff_sequence = golden_backoff(max_retries=retries, base_delay=base_delay)
            for attempt, delay in backoff_sequence:
                try:
                    return func(*args, **kwargs)
                except exceptions as err:
                    if attempt >= retries:
                        raise err
                    time.sleep(max(0.05, delay))
            return None
        return wrapper
    return decorator

@retry_network_op(exceptions=(ConnectionError, TimeoutError, OSError), retries=4)
def execute_resilient_request(action: Callable[[], Any]) -> Any:
    """Executes a given network action with golden ratio retry protection."""
    return action()
