import functools
from typing import Any, Callable, Dict

class DataTransformer:
    def __init__(self, mapping: Dict[str, str]):
        self._mapping = mapping

    def __call__(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {self._mapping.get(k, k): v for k, v in data.items()}

def compose(*functions: Callable) -> Callable:
    return functools.reduce(lambda f, g: lambda x: g(f(x)), functions, lambda x: x)

def memoize_data(func: Callable) -> Callable:
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        key = str(args)
        if key not in cache:
            cache[key] = func(*args)
        return cache[key]
    return wrapper

def deep_extract(data: Any, path: str, default: Any = None) -> Any:
    keys = path.split('.')
    for key in keys:
        if isinstance(data, dict):
            data = data.get(key, default)
        elif isinstance(data, list) and key.isdigit():
            try:
                data = data[int(key)]
            except IndexError:
                return default
        else:
            return default
    return data

def sanitize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in payload.items() if v is not None}