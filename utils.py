from typing import Any, Callable, Dict, List, Union


class DataPipe:
    """A fluent pipeline wrapper chaining data handling functions via standard operators."""

    def __init__(self, func: Callable[[Any], Any]):
        self.func = func

    def __call__(self, data: Any) -> Any:
        return self.func(data)

    def __rshift__(self, other: Union[Callable[[Any], Any], "DataPipe"]) -> "DataPipe":
        next_func = other.func if isinstance(other, DataPipe) else other
        return DataPipe(lambda x: next_func(self.func(x)))


def flatten_structure(d: Dict[str, Any], parent_key: str = "", sep: str = ".") -> Dict[str, Any]:
    """Recursively flattens complex nested dictionary and list collections."""
    items: List[tuple] = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else str(k)
        if isinstance(v, dict):
            items.extend(flatten_structure(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for idx, item in enumerate(v):
                if isinstance(item, dict):
                    items.extend(flatten_structure(item, f"{new_key}[{idx}]", sep=sep).items())
                else:
                    items.append((f"{new_key}[{idx}]", item))
        else:
            items.append((new_key, v))
    return dict(items)


def coerce_primitives(data: Any) -> Any:
    """Recursively casts stringified representations into native Python primitives."""
    if isinstance(data, dict):
        return {k: coerce_primitives(v) for k, v in data.items()}
    if isinstance(data, list):
        return [coerce_primitives(elem) for elem in data]
    if isinstance(data, str):
        normalized = data.strip().lower()
        if normalized == "true":
            return True
        if normalized == "false":
            return False
        if normalized in ("none", "null"):
            return None
        try:
            return int(data)
        except ValueError:
            try:
                return float(data)
            except ValueError:
                return data
    return data


# Chained transformation sequence for standardized dynamic data morphing
clean_and_flatten = DataPipe(coerce_primitives) >> DataPipe(flatten_structure)


def sanitize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Utility function to sanitize and flatten arbitrary dynamic raw payloads."""
    return clean_and_flatten(payload)
