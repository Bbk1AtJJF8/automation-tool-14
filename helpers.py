from functools import reduce
from typing import Any, Callable, Iterable, List, Dict


class Pipe:
    """Wrapper enabling pipe syntax (data | Pipe(func)) for fluent data processing."""
    def __init__(self, func: Callable[..., Any]):
        self.func = func

    def __ror__(self, other: Any) -> Any:
        return self.func(other)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.func(*args, **kwargs)


@Pipe
def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    """Recursively flatten nested dictionaries into single-level dot-notated dicts."""
    items: List[tuple] = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else str(k)
        if isinstance(v, dict):
            items.extend(flatten_dict(v, parent_key=new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


@Pipe
def chunk_stream(iterable: Iterable[Any], size: int = 5) -> List[List[Any]]:
    """Split an iterable into fixed-size chunks using generator reduction."""
    lst = list(iterable)
    return [lst[i:i + size] for i in range(0, len(lst), size)]


def coalesce(*args: Any, default: Any = None) -> Any:
    """Return the first non-None argument or default."""
    return next((arg for arg in args if arg is not None), default)


def execute_pipeline(data: Any, *steps: Callable[[Any], Any]) -> Any:
    """Execute a sequence of transformations on initial data sequentially."""
    return reduce(lambda val, func: func(val), steps, data)
