import functools
import re
from typing import Any, Callable, List

class Flow:
    """A monadic-style functional wrapper for composing data transformations."""

    def __init__(self, fn: Callable[[Any], Any]):
        self.fn = fn

    def __or__(self, next_fn: Callable[[Any], Any]) -> "Flow":
        @functools.wraps(next_fn)
        def combined(data: Any) -> Any:
            return next_fn(self.fn(data))
        return Flow(combined)

    def __call__(self, data: Any) -> Any:
        return self.fn(data)

def strip_and_lower(text: Any) -> str:
    return str(text).strip().lower()

def remove_special_chars(text: str) -> str:
    return re.sub(r"[^\w\s-]", "", text)

def normalize_spaces(text: str) -> str:
    return " ".join(text.split())

def truncate(limit: int) -> Callable[[str], str]:
    return lambda text: text[:limit] if len(text) > limit else text

# Reorganized helper pipelines for standard workflow cleanup
clean_text = Flow(strip_and_lower) | remove_special_chars | normalize_spaces
clean_slug = clean_text | (lambda t: t.replace(" ", "-")) | truncate(50)

def batch_transform(items: List[Any], pipeline: Flow = clean_text) -> List[Any]:
    """Applies composed transformation pipeline across an iterable."""
    return [pipeline(item) for item in items if item is not None]
