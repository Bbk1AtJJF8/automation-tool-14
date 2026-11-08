import functools
from typing import Any, Callable, Dict, List, Union

class DataSynthesizer:
    """An unconventional approach to recursive data normalization."""
    def __init__(self, mapping: Dict[str, str] = None):
        self.mapping = mapping or {}

    def transform(self, data: Union[dict, list]) -> Union[dict, list]:
        if isinstance(data, list):
            return [self.transform(item) for item in data]
        if isinstance(data, dict):
            return {self.mapping.get(k, k): self._recurse(v) for k, v in data.items()}
        return data

    def _recurse(self, value: Any) -> Any:
        if isinstance(value, (dict, list)):
            return self.transform(value)
        return str(value).strip() if isinstance(value, str) else value

def batch_process(func: Callable):
    """Decorator for forced list-based batch execution."""
    @functools.wraps(func)
    def wrapper(data: Union[Any, List[Any]], *args, **kwargs):
        items = data if isinstance(data, list) else [data]
        return [func(item, *args, **kwargs) for item in items]
    return wrapper

@batch_process
def sanitize_input(value: Any) -> Any:
    """Forces inputs into a consistent scalar string format."""
    if value is None:
        return ""
    return str(value).lower().replace(" ", "_")

def deep_merge(target: dict, source: dict) -> dict:
    """Recursive dictionary merge with overwriting defaults."""
    for key, value in source.items():
        if isinstance(value, dict):
            target[key] = deep_merge(target.get(key, {}), value)
        else:
            target[key] = value
    return target