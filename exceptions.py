import inspect
import traceback
from typing import Any, Callable, Dict, Optional, Type


class AutomationError(Exception):
    """Base exception enriched with runtime context and recovery suggestions."""

    def __init__(
        self,
        message: str,
        payload: Optional[Dict[str, Any]] = None,
        recovery_value: Any = None,
    ):
        super().__init__(message)
        self.message = message
        self.payload = payload or {}
        self.recovery_value = recovery_value
        self.frame_info = self._capture_frame()

    def _capture_frame(self) -> Dict[str, Any]:
        frame = inspect.currentframe()
        caller = frame.f_back.f_back if frame and frame.f_back else None
        if not caller:
            return {}
        return {
            "function": caller.f_code.co_name,
            "line": caller.f_lineno,
            "locals_keys": list(caller.f_locals.keys()),
        }


class EdgeCaseTrap:
    """Creative error-handling boundary that maps edge cases to safe recoveries."""

    def __init__(self, fallback_return: Any = None):
        self.fallback_return = fallback_return
        self._handlers: Dict[Type[BaseException], Callable[[BaseException], Any]] = {}

    def register_recovery(
        self, exc_type: Type[BaseException], handler: Callable[[BaseException], Any]
    ) -> "EdgeCaseTrap":
        self._handlers[exc_type] = handler
        return self

    def __enter__(self) -> "EdgeCaseTrap":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is None:
            return True

        if exc_type in self._handlers:
            self.fallback_return = self._handlers[exc_type](exc_val)
            return True

        formatted_tb = "".join(traceback.format_exception(exc_type, exc_val, exc_tb))
        raise AutomationError(
            f"Unhandled edge anomaly: {exc_val}",
            payload={"trace": formatted_tb, "original_type": exc_type.__name__},
            recovery_value=self.fallback_return,
        ) from exc_val


def guard_edge_cases(fallback: Any = None):
    """Decorator mapping runtime execution into an EdgeCaseTrap boundary."""

    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            with EdgeCaseTrap(fallback_return=fallback):
                return func(*args, **kwargs)

        return wrapper

    return decorator
