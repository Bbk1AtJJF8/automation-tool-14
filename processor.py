import random
import time
import urllib.error
import urllib.request
from typing import Any, Callable, Generator, TypeVar

T = TypeVar("T")


def _fibonacci_jitter_delay(
    base: float = 0.5, cap: float = 10.0
) -> Generator[float, None, None]:
    a, b = 1, 1
    while True:
        jitter = random.uniform(0.8, 1.2)
        delay = min(cap, (a * base) * jitter)
        yield delay
        a, b = b, a + b


def network_retry(
    max_attempts: int = 4,
    backoff_cap: float = 8.0,
    retryable_codes: tuple = (408, 429, 500, 502, 503, 504),
):
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        def wrapper(*args: Any, **kwargs: Any) -> T:
            delays = _fibonacci_jitter_delay(cap=backoff_cap)
            attempts = 0
            while True:
                attempts += 1
                try:
                    return func(*args, **kwargs)
                except urllib.error.HTTPError as err:
                    if err.code not in retryable_codes or attempts >= max_attempts:
                        raise
                except (urllib.error.URLError, TimeoutError, ConnectionError):
                    if attempts >= max_attempts:
                        raise

                wait_time = next(delays)
                time.sleep(wait_time)

        return wrapper

    return decorator


@network_retry(max_attempts=3, backoff_cap=5.0)
def fetch_endpoint(url: str, timeout: float = 5.0) -> str:
    req = urllib.request.Request(
        url, headers={"User-Agent": "AutomationTool14/1.0"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read().decode("utf-8")
