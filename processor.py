import functools
from typing import Any, Callable, Dict, List, Union

class ProcessPipe:
    """Creative data processing pipe using bitwise operators for chaining."""

    def __init__(self, step: Callable[[Any], Any] = lambda x: x):
        self._step = step

    def __call__(self, data: Any) -> Any:
        return self._step(data)

    def __or__(self, next_step: Union[Callable, 'ProcessPipe']) -> 'ProcessPipe':
        func = next_step._step if isinstance(next_step, ProcessPipe) else next_step
        return ProcessPipe(lambda d: func(self._step(d)))

    def __rshift__(self, key_path: str) -> 'ProcessPipe':
        """Extract deeply nested dictionary key or list index using dot notation."""
        def extract(data: Any) -> Any:
            curr = data
            for key in key_path.split('.'):
                if isinstance(curr, dict) and key in curr:
                    curr = curr[key]
                elif isinstance(curr, (list, tuple)) and key.isdigit():
                    idx = int(key)
                    curr = curr[idx] if 0 <= idx < len(curr) else None
                else:
                    return None
            return curr
        return self | ProcessPipe(extract)

def flatten_structure(data: Any, prefix: str = '', sep: str = '/') -> Dict[str, Any]:
    """Recursively flattens nested dicts and lists into single-level keys."""
    items: Dict[str, Any] = {}
    if isinstance(data, dict):
        for k, v in data.items():
            new_key = f"{prefix}{sep}{k}" if prefix else str(k)
            items.update(flatten_structure(v, new_key, sep=sep))
    elif isinstance(data, (list, tuple)):
        for idx, item in enumerate(data):
            new_key = f"{prefix}{sep}{idx}" if prefix else str(idx)
            items.update(flatten_structure(item, new_key, sep=sep))
    else:
        items[prefix] = data
    return items

def batch_transform(records: List[Dict[str, Any]], pipeline: ProcessPipe) -> List[Any]:
    """Transforms a stream of records through a custom ProcessPipe pipeline."""
    return [pipeline(record) for record in records if record is not None]
