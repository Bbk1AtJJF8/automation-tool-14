from typing import Any, Callable, Dict, List, Union
from functools import reduce
import operator

def deep_reach(data: Dict, path: str, default: Any = None) -> Any:
    """navigates nested dictionary structures using dot notation"""
    try:
        return reduce(operator.getitem, path.split('.'), data)
    except (KeyError, TypeError, AttributeError):
        return default

def sanitize_stream(data: List[Union[Dict, Any]], keys: List[str]) -> List[Dict]:
    """filters dictionary lists keeping only defined keys"""
    return [{k: v for k, v in item.items() if k in keys} 
            for item in data if isinstance(item, dict)]

def transform_batch(data: List[Dict], mapper: Callable[[Dict], Dict]) -> List[Dict]:
    """applies functional mapping across data payloads"""
    return list(map(mapper, data))

def coalesce_values(*args: Any) -> Any:
    """returns first non-none value in sequence"""
    return next((x for x in args if x is not None), None)

class DataPipeline:
    def __init__(self, data: List[Any]):
        self._payload = data

    def __call__(self, pipeline_fn: Callable[[List[Any]], Any]) -> Any:
        return pipeline_fn(self._payload)

    def flatten(self) -> 'DataPipeline':
        self._payload = [item for sublist in self._payload for item in sublist]
        return self