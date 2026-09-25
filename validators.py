import re
from typing import Any, Callable, Dict, List, Union

def sanitize_input(data: Any, schema: Dict[str, Callable]) -> Dict[str, Any]:
    """Dynamic pipeline for data shape enforcement."""
    processed = {}
    for key, validator in schema.items():
        value = data.get(key)
        try:
            processed[key] = validator(value) if value is not None else None
        except Exception:
            processed[key] = None
    return processed

def chain_validators(*funcs: Callable) -> Callable:
    """Functional composition of data inspection logic."""
    def wrapper(val: Any) -> Any:
        for f in funcs:
            val = f(val)
        return val
    return wrapper

def is_email(val: str) -> Union[str, None]:
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return val if isinstance(val, str) and re.match(pattern, val) else None

def to_int(val: Any) -> Union[int, None]:
    try:
        return int(val)
    except (ValueError, TypeError):
        return None

if __name__ == '__main__':
    schema = {
        'id': to_int,
        'email': is_email,
        'score': chain_validators(to_int, lambda x: max(0, min(x or 0, 100)))
    }
    sample = {'id': '123', 'email': 'test@example.com', 'score': '150'}
    print(sanitize_input(sample, schema))