import json
from typing import Any, Callable, Dict, List, Union
from functools import reduce

def deep_get(data: Dict, path: str, default: Any = None) -> Any:
    """navigates dictionary trees via dot-notation string paths"""
    try:
        return reduce(lambda d, key: d.get(key, {}) if isinstance(d, dict) else default, path.split('.'), data)
    except (AttributeError, TypeError):
        return default

def transform_data(data: List[Dict], mapper: Dict[str, Callable]) -> List[Dict]:
    """applies functional mapping to list of dictionaries"""
    return [{k: func(item.get(k)) for k, func in mapper.items()} for item in data]

def sanitize_input(value: Any) -> Any:
    """recursive stripper of whitespace for data integrity"""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        return {k: sanitize_input(v) for k, v in value.items()}
    if isinstance(value, list):
        return [sanitize_input(v) for v in value]
    return value

def serialize_safe(obj: Any) -> str:
    """json serialization with fallback string conversion"""
    return json.dumps(obj, default=str)