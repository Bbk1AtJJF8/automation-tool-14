import random
import time
import urllib.error
import urllib.request
from typing import Any, Callable, Generator


def _fibonacci_jitter_backoff(
    max_retries: int = 4, base_delay: float = 0.5
) -> Generator[float, None, None]:
    a, b = base_delay, base_delay
    for _ in range(max_retries):
        jitter = random.uniform(0.8, 1.2)
        yield a * jitter
        a, b = b, a + b


class NetworkProcessor:
    """Executes network calls with dynamic generator-driven retry strategies."""

    def __init__(
        self,
        backoff_factory: Callable[
            [], Generator[float, None, None]
        ] = _fibonacci_jitter_backoff,
    ):
        self.backoff_factory = backoff_factory

    def execute_with_retry(
        self, url: str, timeout: float = 3.0
    ) -> dict[str, Any]:
        delays = self.backoff_factory()
        attempt = 1

        while True:
            try:
                req = urllib.request.Request(
                    url, headers={"User-Agent": "AutomationTool14/1.0"}
                )
                with urllib.request.urlopen(req, timeout=timeout) as response:
                    return {
                        "status": response.status,
                        "data": response.read().decode("utf-8"),
                        "attempts": attempt,
                    }
            except (urllib.error.URLError, TimeoutError, OSError) as exc:
                try:
                    delay = next(delays)
                except StopIteration:
                    raise RuntimeError(
                        f"Network operation failed after {attempt} attempts: {exc}"
                    ) from exc

                time.sleep(delay)
                attempt += 1


def fetch_payload(endpoint: str) -> dict[str, Any]:
    processor = NetworkProcessor()
    return processor.execute_with_retry(endpoint)
