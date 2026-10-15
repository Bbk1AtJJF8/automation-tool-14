import math
from typing import Any, Callable, Dict


class ResilienceBoundary:
    """Creative error boundary that dynamically sanitizes edge-case payloads."""

    def __init__(self, fallback_factory: Callable[[Exception, tuple, dict], Any]):
        self.fallback_factory = fallback_factory

    def __call__(self, func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                sanitized_args = tuple(self._sanitize(a) for a in args)
                sanitized_kwargs = {
                    k: self._sanitize(v) for k, v in kwargs.items()
                }
                return func(*sanitized_args, **sanitized_kwargs)
            except (
                ZeroDivisionError,
                ValueError,
                TypeError,
                RecursionError,
            ) as err:
                return self.fallback_factory(err, args, kwargs)

        return wrapper

    def _sanitize(self, val: Any) -> Any:
        if isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
            return 0.0
        if isinstance(val, (bytes, bytearray)):
            return val.decode("utf-8", errors="replace")
        if val is None:
            return ""
        return val


def adaptive_recovery(
    exc: Exception, args: tuple, kwargs: dict
) -> Dict[str, Any]:
    """Generates a structured recovery object when edge cases break execution."""
    return {
        "status": "degraded",
        "error_type": type(exc).__name__,
        "error_message": str(exc),
        "recovered_value": args[0] if args else kwargs.get("default", None),
    }


@ResilienceBoundary(fallback_factory=adaptive_recovery)
def process_pipeline_data(data_stream: Any, threshold: float = 1.0) -> float:
    """Processes pipeline data with edge-case protection."""
    if not isinstance(data_stream, (int, float, str)):
        raise TypeError(f"Unsupported payload type: {type(data_stream)}")

    numeric_val = float(data_stream)
    return round(100.0 / numeric_val, 4) * threshold
