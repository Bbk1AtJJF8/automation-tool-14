from collections.abc import Mapping, Iterable
from typing import Any, Callable, Dict


class DataWeaver:
    """Fluid dynamic transformer for nested data structures using pipeline operators."""

    def __init__(self, data: Any):
        self.data = data

    def extract_paths(self, prefix: str = "") -> Dict[str, Any]:
        """Recursively flattens nested dicts and lists into key-path notation."""
        out = {}
        if isinstance(self.data, Mapping):
            for k, v in self.data.items():
                p = f"{prefix}.{k}" if prefix else str(k)
                out.update(DataWeaver(v).extract_paths(p))
        elif isinstance(self.data, Iterable) and not isinstance(self.data, (str, bytes)):
            for idx, item in enumerate(self.data):
                p = f"{prefix}[{idx}]"
                out.update(DataWeaver(item).extract_paths(p))
        else:
            out[prefix] = self.data
        return out

    def __rshift__(self, func: Callable[[Any], Any]) -> "DataWeaver":
        """Overloaded >> operator to pipe dynamic transformations."""
        return DataWeaver(func(self.data)) if callable(func) else self

    def prune(self, predicate: Callable[[Any], bool] = lambda x: x is None) -> "DataWeaver":
        """Recursively purges elements matching predicate condition."""
        def _clean(obj):
            if isinstance(obj, dict):
                return {k: _clean(v) for k, v in obj.items() if not predicate(v)}
            elif isinstance(obj, list):
                return [_clean(v) for v in obj if not predicate(v)]
            return obj
        return DataWeaver(_clean(self.data))

    def unwrap(self) -> Any:
        return self.data


def weave(data: Any) -> DataWeaver:
    return DataWeaver(data)
