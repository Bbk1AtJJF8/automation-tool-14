import math
import logging
from typing import Callable, Any, List, Tuple

logger = logging.getLogger("automation.handler")


class EdgeCaseHandler:
    """Dynamic resilient dispatcher for handling automation edge cases."""

    def __init__(self, fallback_value: Any = None):
        self.fallback_value = fallback_value
        self._handlers: List[Tuple[Callable[[Exception], bool], Callable[[Exception], Any]]] = []
        self._register_default_predicates()

    def register(self, predicate: Callable[[Exception], bool], recovery: Callable[[Exception], Any]):
        self._handlers.append((predicate, recovery))

    def _register_default_predicates(self):
        self.register(
            lambda e: isinstance(e, (ZeroDivisionError, ValueError)) and "math" in str(e).lower(),
            lambda e: 0.0
        )
        self.register(
            lambda e: isinstance(e, (IndexError, KeyError, TypeError)),
            lambda e: self.fallback_value
        )
        self.register(
            lambda e: isinstance(e, (OSError, MemoryError)),
            lambda e: logger.warning("System constraint encountered: %s", e) or self.fallback_value
        )

    def execute(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        try:
            result = func(*args, **kwargs)
            if isinstance(result, float) and (math.isnan(result) or math.isinf(result)):
                raise ValueError("math domain edge case: produced invalid float")
            return result
        except Exception as exc:
            for predicate, recovery in self._handlers:
                if predicate(exc):
                    return recovery(exc)
            logger.error("Unhandled edge case in %s: %s", getattr(func, '__name__', 'callable'), exc)
            return self.fallback_value

    def wrap(self, func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return self.execute(func, *args, **kwargs)
        return wrapper


def safe_run(func: Callable, fallback: Any = None, *args: Any, **kwargs: Any) -> Any:
    handler = EdgeCaseHandler(fallback_value=fallback)
    return handler.execute(func, *args, **kwargs)
