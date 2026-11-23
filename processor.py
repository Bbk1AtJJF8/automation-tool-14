"""Dynamic stream execution pipeline with operator overloading."""

from typing import TypeVar, Generic, Callable, Iterator, Iterable, Any
import time

T = TypeVar("T")
R = TypeVar("R")


class PipelineNode(Generic[T, R]):
    """An executable step within an automation processing pipeline.

    Attributes:
        func: Transformation callback applied to inbound stream items.
        delay: Inter-element throttle time specified in seconds.
    """

    def __init__(self, func: Callable[[T], R], delay: float = 0.0) -> None:
        self.func: Callable[[T], R] = func
        self.delay: float = delay

    def __call__(self, item: T) -> R:
        """Executes single item transformation with throttling support."""
        if self.delay > 0:
            time.sleep(self.delay)
        return self.func(item)

    def __or__(self, next_func: Callable[[R], Any]) -> "PipelineNode[T, Any]":
        """Pipes output directly into another callable using the bitwise OR operator."""
        def chained(item: T) -> Any:
            return next_func(self(item))
        return PipelineNode(chained, delay=self.delay)


class StreamProcessor(Generic[T]):
    """Stream processing runtime managing sequential item evaluation."""

    def __init__(self, items: Iterable[T]) -> None:
        self._stream: Iterator[T] = iter(items)

    def process_through(self, node: PipelineNode[T, R]) -> Iterator[R]:
        """Yields transformed results lazily from the stream pipeline.

        Args:
            node: Pipeline node or chained set of execution steps.

        Yields:
            Transformed element from the underlying collection.
        """
        for item in self._stream:
            yield node(item)


def batch_accumulator(source: Iterable[Any], batch_size: int = 3) -> Iterator[list[Any]]:
    """Groups continuous iterable streams into discrete arrays.

    Args:
        source: Iterable data source.
        batch_size: Maximum items per aggregated sequence.

    Yields:
        Slices of elements gathered into fixed-capacity lists.
    """
    batch: list[Any] = []
    for item in source:
        batch.append(item)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    if batch:
        yield batch
