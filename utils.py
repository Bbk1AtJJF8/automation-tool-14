import functools
from typing import Any, Callable, Dict, List, Union

def compose_data_processor(*funcs: Callable) -> Callable:
    """Chain functions as a pipeline for data transformation."""
    return lambda x: functools.reduce(lambda v, f: f(v), funcs, x)

def flatten_deep(data: Union[List, Dict]) -> List[Any]:
    """Recursive flattening of nested structures into a list."""
    flat = []
    items = data.values() if isinstance(data, dict) else data
    for item in items:
        if isinstance(item, (list, dict)):
            flat.extend(flatten_deep(item))
        else:
            flat.append(item)
    return flat

def memoize_data_query(func: Callable) -> Callable:
    """Cache result of function based on arguments."""
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

def smart_sanitize(data: Any, filter_val: Any = None) -> Any:
    """Remove all occurrences of a filter value."""
    if isinstance(data, list):
        return [smart_sanitize(i, filter_val) for i in data if i != filter_val]
    if isinstance(data, dict):
        return {k: smart_sanitize(v, filter_val) for k, v in data.items() if v != filter_val}
    return data if data != filter_val else None