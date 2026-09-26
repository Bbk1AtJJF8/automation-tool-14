"""Helper functions and dynamic pipeline wrappers for data transformations."""

from typing import Any, Callable, Iterable, List


class Pipeable:
    """Enables Unix-style pipe syntax (|) for modular automation functions."""

    def __init__(self, function: Callable[..., Any]):
        self.function = function

    def __ror__(self, left_operand: Any) -> Any:
        return self.function(left_operand)

    def __call__(self, *args: Any, **kwargs: Any) -> "Pipeable":
        return Pipeable(lambda x: self.function(x, *args, **kwargs))


@Pipeable
def safe_traverse(target: Any, dot_path: str, fallback: Any = None) -> Any:
    """Traverses nested dicts or objects via dot-notation path string."""
    for key in dot_path.split("."):
        if isinstance(target, dict):
            target = target.get(key)
        elif hasattr(target, key):
            target = getattr(target, key)
        else:
            return fallback
        if target is None:
            return fallback
    return target


@Pipeable
def chunk_iterable(iterable: Iterable[Any], size: int) -> List[List[Any]]:
    """Splits an iterable into fixed-size chunks."""
    items = list(iterable)
    if size <= 0:
        return [items]
    return [items[i : i + size] for i in range(0, len(items), size)]


def first_non_null(*args: Any, default: Any = None) -> Any:
    """Returns the first non-None argument or fallback default."""
    return next((val for val in args if val is not None), default)
