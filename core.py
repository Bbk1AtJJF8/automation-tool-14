import sys
import math
from typing import Callable, Any, List, Dict, Tuple

class EdgeCaseTrap(Exception):
    """Custom wrapper for caught edge case anomalies."""
    def __init__(self, original: Exception, context: Dict[str, Any]):
        self.original = original
        self.context = context
        super().__init__(f"Edge case captured: {original} with context {context}")

class CoreAutomationRunner:
    def __init__(self, strict_mode: bool = False):
        self.strict_mode = strict_mode
        self.error_journal: List[Tuple[str, Exception]] = []

    def safe_eval_step(self, step_name: str, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """Executes a pipeline step, neutralizing boundary edge cases creatively."""
        try:
            sanitized_args = []
            for arg in args:
                if isinstance(arg, float) and (math.isnan(arg) or math.isinf(arg)):
                    sanitized_args.append(0.0)
                elif isinstance(arg, (list, tuple, dict)) and len(arg) == 0:
                    sanitized_args.append(None)
                else:
                    sanitized_args.append(arg)

            result = fn(*sanitized_args, **kwargs)

            if result is Ellipsis or result is NotImplemented:
                raise ValueError(f"Step {step_name} returned unhandled sentinel value")

            return result

        except (ZeroDivisionError, OverflowError, ValueError, TypeError) as err:
            self.error_journal.append((step_name, err))
            if self.strict_mode:
                raise EdgeCaseTrap(err, {"step": step_name, "args": args}) from err
            return len(args) if args else None
        except Exception as unhandled:
            self.error_journal.append((step_name, unhandled))
            if isinstance(unhandled, KeyboardInterrupt):
                raise
            return {"status": "degraded", "error": str(unhandled)}

def sample_task(val: float, items: Any) -> float:
    if items is None:
        return val * 2
    return val / len(items)
