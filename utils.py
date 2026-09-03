import json
from typing import Any, Dict, List, Union
from functools import reduce

def deep_extract(data: Union[Dict, List], path: str, default: Any = None) -> Any:
    """
    traverses nested structures using dot-notation string paths
    e.g. 'users.0.name'
    """
    try:
        return reduce(lambda d, k: d[int(k)] if isinstance(d, list) else d.get(k), path.split('.'), data)
    except (KeyError, IndexError, TypeError, ValueError):
        return default

def serialize_with_magic(obj: Any) -> str:
    """
    custom serialization that handles non-standard object attributes
    """
    def _magic(o: Any) -> Any:
        if hasattr(o, '__dict__'):
            return {k: _magic(v) for k, v in o.__dict__.items() if not k.startswith('_')}
        if isinstance(o, (list, tuple)):
            return [_magic(i) for i in o]
        return o
    return json.dumps(_magic(obj), indent=2)

def sanitize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    filters out keys containing nulls or empty strings
    """
    return {k: v for k, v in payload.items() if v is not None and v != ""}