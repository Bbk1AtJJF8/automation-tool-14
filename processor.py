import time
from collections import deque
from typing import Callable, Any, Generator, List


class FastBatchProcessor:
    """Adaptive stream processor utilizing slot pooling and dynamic batch tuning."""

    __slots__ = ("_pipeline", "_buffer", "_batch_size", "_target_latency", "_pool")

    def __init__(self, batch_size: int = 64, target_latency_ms: float = 5.0):
        self._pipeline: List[Callable[[Any], Any]] = []
        self._buffer: deque = deque()
        self._batch_size = batch_size
        self._target_latency = target_latency_ms / 1000.0
        self._pool: List[list] = [[] for _ in range(16)]

    def pipe(self, fn: Callable[[Any], Any]) -> "FastBatchProcessor":
        self._pipeline.append(fn)
        return self

    def _acquire_container(self) -> list:
        return self._pool.pop() if self._pool else []

    def _release_container(self, container: list) -> None:
        container.clear()
        if len(self._pool) < 32:
            self._pool.append(container)

    def process_stream(self, items: Generator[Any, None, None]) -> Generator[Any, None, None]:
        fns = tuple(self._pipeline)
        b_size = self._batch_size
        buf = self._buffer

        for item in items:
            buf.append(item)
            if len(buf) >= b_size:
                start_t = time.perf_counter()
                chunk = self._acquire_container()
                while buf:
                    val = buf.popleft()
                    for fn in fns:
                        val = fn(val)
                    chunk.append(val)

                elapsed = time.perf_counter() - start_t
                if elapsed > self._target_latency and b_size > 8:
                    b_size = max(8, b_size - 4)
                elif elapsed < self._target_latency * 0.5 and b_size < 512:
                    b_size += 8
                self._batch_size = b_size

                yield from chunk
                self._release_container(chunk)

        if buf:
            chunk = self._acquire_container()
            while buf:
                val = buf.popleft()
                for fn in fns:
                    val = fn(val)
                chunk.append(val)
            yield from chunk
            self._release_container(chunk)
