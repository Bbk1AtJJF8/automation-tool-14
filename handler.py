import functools
from typing import Any, Callable, Dict, List, Union

def pipe(data: Any, *funcs: Callable) -> Any:
    """a functional pipeline for data transformation."""
    return functools.reduce(lambda v, f: f(v), funcs, data)

def sanitize(data: Union[Dict, List]) -> Union[Dict, List]:
    """deep recursive cleaning of empty values."""
    if isinstance(data, dict):
        return {k: sanitize(v) for k, v in data.items() if v is not None}
    if isinstance(data, list):
        return [sanitize(i) for i in data if i is not None]
    return data

def memoize_data(func: Callable) -> Callable:
    """a decorator for caching process results."""
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        key = str(args)
        if key not in cache:
            cache[key] = func(*args)
        return cache[key]
    return wrapper

def flatten(data: List) -> List:
    """a nested list unrolling sequence."""
    result = []
    for item in data:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result