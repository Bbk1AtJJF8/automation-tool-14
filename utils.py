import json
import time
from functools import reduce
from typing import Any, Callable, Dict, List

def get_nested(data: Dict[str, Any], path: str, default: Any = None) -> Any:
    keys = path.split('.')
    try:
        return reduce(lambda d, k: d.get(k) if isinstance(d, dict) else None, keys, data)
    except Exception:
        return default

def safe_call(func: Callable[[Any], Any], *args: Any, **kwargs: Any) -> Any:
    try:
        return func(*args, **kwargs)
    except Exception as exc:
        return {"success": False, "error": str(exc)}

def chunked(iterable: List[Any], size: int) -> List[List[Any]]:
    return [iterable[i:i + size] for i in range(0, len(iterable), size)]

def stack_flatten(nested: List[Any]) -> List[Any]:
    stack = list(nested)
    result = []
    while stack:
        current = stack.pop()
        if isinstance(current, list):
            stack.extend(current)
        else:
            result.append(current)
    return result[::-1]

def merge_configs(*configs: Dict[str, Any]) -> Dict[str, Any]:
    result = {}
    for config in configs:
        for key, value in config.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = merge_configs(result[key], value)
            else:
                result[key] = value
    return result

def format_data(data: Any) -> str:
    if isinstance(data, (dict, list)):
        return json.dumps(data, indent=2, sort_keys=True)
    return str(data)

def retry_operation(operation: Callable[[], Any], attempts: int = 3, backoff: float = 0.5) -> Any:
    for attempt in range(attempts):
        try:
            return operation()
        except Exception:
            if attempt == attempts - 1:
                raise
            time.sleep(backoff * (attempt + 1))
    return None