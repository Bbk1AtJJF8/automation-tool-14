import json
from typing import Any, Dict, Union
from functools import reduce

def deep_reach(data: Dict[str, Any], path: str, delimiter: str = '.') -> Any:
    """navigates nested dicts using a path string"""
    try:
        return reduce(lambda d, key: d[key] if isinstance(d, dict) else None, path.split(delimiter), data)
    except (KeyError, TypeError):
        return None

def sanitize_payload(payload: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
    """coerces input into a clean dictionary object"""
    if isinstance(payload, str):
        try:
            return json.loads(payload)
        except json.JSONDecodeError:
            return {}
    return dict(payload) if isinstance(payload, dict) else {}

def transform_stream(data: Dict[str, Any], mapping: Dict[str, str]) -> Dict[str, Any]:
    """maps data keys based on transformation schema"""
    return {target: deep_reach(data, source) for target, source in mapping.items()}

class DataPipe:
    """fluent interface for processing arbitrary datasets"""
    def __init__(self, data: Any):
        self.data = sanitize_payload(data)
    
    def extract(self, path: str) -> 'DataPipe':
        return DataPipe(deep_reach(self.data, path) or {})
    
    def serialize(self) -> str:
        return json.dumps(self.data)