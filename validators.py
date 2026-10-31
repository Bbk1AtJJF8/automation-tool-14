import re
from typing import Any, Callable

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))

def soft_coerce(val: Any, target_type: type, default: Any = None) -> Any:
    try:
        return target_type(val)
    except (ValueError, TypeError):
        return default

def chain_validators(value: Any, *validators: Callable[[Any], bool]) -> bool:
    return all(v(value) for v in validators)

def length_range(min_len: int, max_len: int) -> Callable[[str], bool]:
    def check(s: str) -> bool:
        return min_len <= len(str(s)) <= max_len
    return check

def regex_validator(pattern: str) -> Callable[[str], bool]:
    return lambda s: bool(re.search(pattern, str(s)))

class DataGuard:
    def __init__(self, data: dict):
        self.data = data

    def require(self, key: str, validator: Callable[[Any], bool]) -> bool:
        val = self.data.get(key)
        return val is not None and validator(val)

def sanitize_alphanumeric(val: str) -> str:
    return re.sub(r'[^a-zA-Z0-9]', '', str(val))