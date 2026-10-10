import functools
import time
from typing import Any, Callable, Dict, Tuple


class AdaptiveCache:
    """Self-adjusting cache based on execution latency trends."""

    def __init__(self, target_latency_ms: float = 10.0, max_size: int = 128):
        self.target_latency = target_latency_ms / 1000.0
        self.max_size = max_size
        self._cache: Dict[Tuple, Tuple[Any, float, float]] = {}
        self.ttl = 1.0

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.monotonic()

            if key in self._cache:
                val, expires, _ = self._cache[key]
                if now < expires:
                    return val

            start_time = time.monotonic()
            result = func(*args, **kwargs)
            duration = time.monotonic() - start_time

            if duration > self.target_latency:
                self.ttl = min(self.ttl * 1.25, 60.0)
            else:
                self.ttl = max(self.ttl * 0.85, 0.2)

            if len(self._cache) >= self.max_size:
                oldest_key = min(self._cache, key=lambda k: self._cache[k][2])
                del self._cache[oldest_key]

            self._cache[key] = (result, now + self.ttl, now)
            return result

        return wrapper


class CorePipeline:
    def __init__(self, multiplier: int = 2):
        self.multiplier = multiplier

    @AdaptiveCache(target_latency_ms=5.0, max_size=64)
    def process_payload(self, raw_data: str, iterations: int = 5) -> str:
        processed = raw_data
        for _ in range(iterations):
            processed = "".join(
                chr((ord(c) + self.multiplier) % 256) for c in processed
            )
        return processed[::-1]
