from typing import Any, Callable, Dict, List, Optional, Tuple


class EdgeCaseResilientProcessor:
    """Automation pipeline processor with adaptive exception boundaries for malformed data."""

    def __init__(self, default_fallbacks: Optional[Dict[type, Any]] = None) -> None:
        self.fallbacks = default_fallbacks or {
            ZeroDivisionError: 0.0,
            KeyError: "MISSING_KEY",
            TypeError: "",
            ValueError: None,
            RecursionError: "MAX_DEPTH_REACHED",
        }

    def guard(self, default_override: Any = ...):
        """Decorator mapping standard and custom runtime anomalies to safe fallback values."""
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    if default_override is not Ellipsis:
                        return default_override
                    for exc_type, safe_val in self.fallbacks.items():
                        if isinstance(exc, exc_type):
                            return safe_val
                    return f"HANDLED_EXC_{exc.__class__.__name__}"
            return wrapper
        return decorator

    def process_item(self, payload: Any, depth: int = 0) -> Any:
        @self.guard()
        def _evaluate(val: Any) -> Any:
            if depth > 15:
                raise RecursionError("Recursion threshold reached")
            if isinstance(val, dict):
                return {k: self.process_item(v, depth + 1) for k, v in val.items()}
            if isinstance(val, (list, tuple)):
                return [self.process_item(x, depth + 1) for x in val]
            if isinstance(val, (int, float)):
                return 1000 / val
            if isinstance(val, str) and val.isnumeric():
                return int(val) * 2
            return str(val)

        return _evaluate(payload)

    def process_pipeline(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        processed_data: List[Any] = []
        recovery_log: List[Tuple[int, str]] = []

        for index, record in enumerate(records):
            @self.guard(default_override={"status": "FAILED_RECORD"})
            def _step() -> Dict[str, Any]:
                if not isinstance(record, dict):
                    raise TypeError("Record must be a dictionary")
                return {
                    "id": record.get("id", index),
                    "value": self.process_item(record.get("value")),
                }

            result = _step()
            if result == {"status": "FAILED_RECORD"}:
                recovery_log.append((index, "Non-dict record payload handled"))
            processed_data.append(result)

        return {
            "total": len(records),
            "recovered": len(recovery_log),
            "results": processed_data,
            "logs": recovery_log,
        }
