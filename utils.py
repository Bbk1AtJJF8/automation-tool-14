"""Dynamic task transformation and pipelining utilities."""

from typing import TypeVar, Callable, Any, Iterable, Generator, Generic
from functools import wraps, reduce
import time

T = TypeVar("T")
R = TypeVar("R")


class PipelineComposer(Generic[T, R]):
    """A creative pipeline composer that chains callables using the bitwise OR operator.

    Allows assembling data processing stages dynamically:
        pipe = PipelineComposer(stage1) | stage2 | stage3
        result = pipe(initial_data)
    """

    def __init__(self, func: Callable[[T], Any]) -> None:
        """Initialize the pipeline with a root callable."""
        self._funcs: list[Callable[[Any], Any]] = [func]

    def __or__(self, next_func: Callable[[Any], Any]) -> "PipelineComposer[T, R]":
        """Overload `|` operator to append transformation stages."""
        new_composer: PipelineComposer[T, R] = PipelineComposer(self._funcs[0])
        new_composer._funcs = self._funcs + [next_func]
        return new_composer

    def __call__(self, initial_value: T) -> R:
        """Execute all chained callables sequentially on the input payload."""
        return reduce(lambda acc, f: f(acc), self._funcs, initial_value)  # type: ignore[return-value]


def pulse_stream(items: Iterable[T], delay: float = 0.01) -> Generator[T, None, None]:
    """Yield items from an iterable with a temporal pulse delay.

    Args:
        items: The collection of items to emit.
        delay: Seconds to sleep between items.

    Yields:
        Individual elements from `items` spaced by `delay`.
    """
    for item in items:
        time.sleep(delay)
        yield item


def retry_with_fallback(
    retries: int = 3, fallback: Callable[..., Any] | None = None
) -> Callable[[Callable[..., R]], Callable[..., R]]:
    """Decorator for retrying a function upon failure, falling back if exhausted.

    Args:
        retries: Maximum number of execution attempts.
        fallback: Optional callable invoked with exception if retries fail.

    Returns:
        Decorated function with automatic retry behavior.
    """

    def decorator(func: Callable[..., R]) -> Callable[..., R]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> R:
            last_err: Exception | None = None
            for _ in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as err:
                    last_err = err
            if fallback is not None and last_err is not None:
                return fallback(last_err, *args, **kwargs)  # type: ignore[no-any-return]
            if last_err:
                raise last_err
            raise RuntimeError("Execution failed without explicit exception")

        return wrapper

    return decorator
