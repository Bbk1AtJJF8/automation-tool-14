import functools
import gc
from typing import Any, Callable, Dict, List, Optional, Tuple


class HelperPipeline:
    """Dynamic helper execution registry with automatic state cleanup."""

    _registry: Dict[str, Callable] = {}
    _transient_cache: Dict[str, Any] = {}

    @classmethod
    def register(cls, alias: Optional[str] = None):
        def decorator(func: Callable) -> Callable:
            name = alias or func.__name__

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                cls._transient_cache[f"{name}_last"] = result
                return result

            cls._registry[name] = wrapper
            return wrapper

        return decorator

    @classmethod
    def purge_transients(cls) -> int:
        """Reorganizes internal memory state by flushing transient cache."""
        count = len(cls._transient_cache)
        cls._transient_cache.clear()
        gc.collect()
        return count

    @classmethod
    def dispatch(cls, step_name: str, *args, **kwargs) -> Any:
        if step_name not in cls._registry:
            raise KeyError(f"Helper step '{step_name}' is not registered.")
        return cls._registry[step_name](*args, **kwargs)


@HelperPipeline.register(alias="sanitize_text")
def _sanitize(text: str) -> str:
    return " ".join(text.strip().split())


@HelperPipeline.register(alias="flatten_dict")
def _flatten(
    d: Dict[str, Any], parent_key: str = "", sep: str = "."
) -> Dict[str, Any]:
    items: List[Tuple[str, Any]] = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(_flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def execute_sequence(data: Any, sequence: List[str]) -> Any:
    """Executes a pipeline sequence and reorganizes memory state after."""
    current = data
    try:
        for step in sequence:
            current = HelperPipeline.dispatch(step, current)
        return current
    finally:
        HelperPipeline.purge_transients()
