import time
from collections import deque
from typing import Callable, Any, Generator


class AdaptiveBatchProcessor:
    """High-throughput processor adjusting batch sizes based on window latency."""

    __slots__ = ("_queue", "_target_latency", "_batch_size", "_processed_count")

    def __init__(self, target_latency: float = 0.05, initial_batch_size: int = 10):
        self._queue: deque = deque()
        self._target_latency: float = target_latency
        self._batch_size: int = max(1, initial_batch_size)
        self._processed_count: int = 0

    def enqueue(self, item: Any) -> None:
        self._queue.append(item)

    def consume_stream(self, worker_fn: Callable[[list], list]) -> Generator[Any, None, None]:
        while self._queue:
            current_batch = [
                self._queue.popleft()
                for _ in range(min(len(self._queue), self._batch_size))
            ]
            t0 = time.perf_counter()
            results = worker_fn(current_batch)
            elapsed = time.perf_counter() - t0

            self._processed_count += len(current_batch)
            self._adjust_batch_size(elapsed, len(current_batch))
            yield from results

    def _adjust_batch_size(self, elapsed: float, count: int) -> None:
        if count == 0:
            return
        per_item = elapsed / count
        if per_item <= 0:
            self._batch_size = min(self._batch_size * 2, 1000)
            return
        ideal_size = max(1, int(self._target_latency / per_item))
        self._batch_size = max(1, int(0.7 * self._batch_size + 0.3 * ideal_size))

    @property
    def stats(self) -> dict:
        return {
            "batch_size": self._batch_size,
            "processed": self._processed_count,
            "pending": len(self._queue),
        }
