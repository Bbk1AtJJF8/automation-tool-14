import functools
from typing import Any, Callable, Dict, Optional

def flexible_data_transformer(pipeline: list = None) -> Callable:
    """Chainable data processing pipeline using closure factories."""
    pipeline = pipeline or []
    
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(data: Any, *args, **kwargs):
            result = data
            for step in pipeline:
                result = step(result)
            return func(result, *args, **kwargs)
        return wrapper
    return decorator

def shallow_denest(data: Dict[str, Any], separator: str = '_') -> Dict[str, Any]:
    """Flatten nested dictionaries into a single depth map."""
    items = {}
    for key, value in data.items():
        if isinstance(value, dict):
            for subkey, subvalue in shallow_denest(value, separator).items():
                items[f"{key}{separator}{subkey}"] = subvalue
        else:
            items[key] = value
    return items

class DataSanitizer:
    def __init__(self, schema: Dict[str, type]):
        self.schema = schema

    def __call__(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Dynamic type casting and schema enforcement tool."""
        return {
            k: (v if isinstance(v, self.schema.get(k, object)) else self.schema.get(k, lambda x: x)(v))
            for k, v in payload.items() if k in self.schema
        }