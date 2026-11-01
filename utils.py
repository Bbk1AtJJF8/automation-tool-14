from typing import Any, Callable, Dict, List, Union


class DataPipe:
    """Pipelined data transformer using bitwise OR operator overloading."""

    def __init__(self, func: Callable[[Any], Any]):
        self.func = func

    def __ror__(self, data: Any) -> Any:
        return self.func(data)

    def __or__(self, next_stage: "DataPipe") -> "DataPipe":
        return DataPipe(lambda x: next_stage.func(self.func(x)))


def deep_pluck(*keys: str) -> DataPipe:
    """Extract nested key paths from complex dicts/lists using dot notation."""
    def _extract(data: Any) -> List[Any]:
        results = []
        for key in keys:
            parts = key.split(".")
            current = data
            for part in parts:
                if isinstance(current, dict) and part in current:
                    current = current[part]
                elif isinstance(current, (list, tuple)) and part.isdigit():
                    idx = int(part)
                    current = current[idx] if 0 <= idx < len(current) else None
                else:
                    current = None
                    break
            results.append(current)
        return results
    return DataPipe(_extract)


def flatten_structure(delimiter: str = "_") -> DataPipe:
    """Flatten deeply nested data structures into single-level dictionary."""
    def _flatten(obj: Any, prefix: str = "") -> Dict[str, Any]:
        items: Dict[str, Any] = {}
        if isinstance(obj, dict):
            for k, v in obj.items():
                new_key = f"{prefix}{delimiter}{k}" if prefix else str(k)
                items.update(_flatten(v, new_key))
        elif isinstance(obj, (list, tuple)):
            for i, v in enumerate(obj):
                new_key = f"{prefix}{delimiter}{i}" if prefix else str(i)
                items.update(_flatten(v, new_key))
        else:
            items[prefix] = obj
        return items
    return DataPipe(_flatten)


def sanitize_values(default: Any = None) -> DataPipe:
    """Clean empty values (None, empty strings, empty containers) recursively."""
    def _clean(obj: Any) -> Any:
        if isinstance(obj, dict):
            return {k: _clean(v) for k, v in obj.items() if v not in (None, "", [], {})}
        elif isinstance(obj, list):
            return [_clean(v) for v in obj if v not in (None, "", [], {})]
        return obj if obj is not None else default
    return DataPipe(_clean)
