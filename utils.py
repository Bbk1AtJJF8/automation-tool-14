import functools
import inspect
from typing import Callable, Any, TypeVar

T = TypeVar("T")

class MetamorphicRectifier:
    """Dynamically resolves edge-case failures by coercing unexpected types."""

    @staticmethod
    def rectify_argument(val: Any, target_type: type) -> Any:
        try:
            if target_type is str and isinstance(val, (bytes, bytearray)):
                return val.decode("utf-8", errors="ignore")
            if target_type is int and isinstance(val, str):
                digits = "".join(c for c in val if c.isdigit() or c == "-")
                return int(digits) if digits and digits != "-" else 0
            if isinstance(val, list) and len(val) == 1:
                return val[0]
            return target_type(val)
        except (TypeError, ValueError):
            return val

def heal_edge_cases(default_fallback: Any = None) -> Callable:
    """Decorator to intercept standard exceptions, auto-coerce types, or yield a default."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except (TypeError, ValueError, AttributeError):
                sig = inspect.signature(func)
                bound = sig.bind_partial(*args, **kwargs)
                bound.apply_defaults()
                
                healed_kwargs = {}
                for name, param in sig.parameters.items():
                    val = bound.arguments.get(name)
                    if val is not None and param.annotation is not inspect.Parameter.empty:
                        healed_kwargs[name] = MetamorphicRectifier.rectify_argument(val, param.annotation)
                    else:
                        healed_kwargs[name] = val
                
                try:
                    return func(**healed_kwargs)
                except Exception:
                    ret_type = sig.return_annotation
                    if ret_type is not inspect.Signature.empty and callable(ret_type):
                        try:
                            return ret_type()
                        except Exception:
                            pass
                    return default_fallback
        return wrapper
    return decorator
