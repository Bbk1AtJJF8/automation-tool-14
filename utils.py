import random
import time
import urllib.error
import urllib.request
from typing import Any, Callable, Tuple, Type


class RetriesExhaustedError(Exception):
    """Raised when all network retry attempts fail."""

    pass


def retry_network_call(
    retries: int = 3,
    base_delay: float = 0.5,
    exceptions: Tuple[Type[Exception], ...] = (
        urllib.error.URLError,
        TimeoutError,
        ConnectionResetError,
    ),
):
    """Decorator utilizing a generator backoff stream for network retry logic."""

    def _backoff_generator():
        current_delay = base_delay
        for attempt in range(1, retries + 1):
            yield attempt, current_delay
            current_delay = random.uniform(base_delay, current_delay * 2.0 + 0.1)

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            for attempt, delay in _backoff_generator():
                try:
                    return func(*args, **kwargs)
                except exceptions as err:
                    last_exception = err
                    if attempt < retries:
                        time.sleep(delay)

            raise RetriesExhaustedError(
                f"Call '{func.__name__}' failed after {retries} retries."
            ) from last_exception

        return wrapper

    return decorator


@retry_network_call(retries=3, base_delay=0.2)
def fetch_resource(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "automation-tool-14"})
    with urllib.request.urlopen(req, timeout=3) as response:
        return response.read().decode("utf-8")
