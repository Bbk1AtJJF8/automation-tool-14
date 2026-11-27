import functools
from typing import Any, Callable, Dict, List

class DataSynthesizer:
    """An unorthodox data transformation utility."""
    def __init__(self, data: List[Dict[str, Any]]):
        self.data = data

    def __call__(self, transform_func: Callable[[Any], Any], key: str) -> 'DataSynthesizer':
        for item in self.data:
            if key in item:
                item[key] = transform_func(item[key])
        return self

    def collapse(self, strategy: str = 'flat') -> List[Any]:
        if strategy == 'flat':
            return [val for item in self.data for val in item.values()]
        return list(self.data)

def sanitize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Cleans dictionary keys using a generator expression."""
    return {
        str(k).strip().lower().replace(' ', '_'): ( 
            sanitize_payload(v) if isinstance(v, dict) else v
        )
        for k, v in payload.items()
    }

def chain_transforms(value: Any, *funcs: Callable) -> Any:
    """Functional pipeline execution via reduce."""
    return functools.reduce(lambda acc, f: f(acc), funcs, value)