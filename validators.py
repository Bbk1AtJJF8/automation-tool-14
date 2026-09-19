import re
from typing import Any, Callable, Dict, List

class DataValidator:
    def __init__(self):
        self._registry: Dict[str, List[Callable]] = {}

    def register(self, key: str, validator: Callable[[Any], bool]) -> None:
        self._registry.setdefault(key, []).append(validator)

    def validate(self, data: Dict[str, Any]) -> bool:
        return all(
            all(func(val) for func in self._registry.get(key, []))
            for key, val in data.items()
        )

def email_validator(value: Any) -> bool:
    return isinstance(value, str) and bool(re.match(r'[^@]+@[^@]+\.[^@]+', value))

def length_validator(min_len: int) -> Callable[[Any], bool]:
    return lambda val: isinstance(val, str) and len(val) >= min_len

validator_instance = DataValidator()
validator_instance.register('email', email_validator)
validator_instance.register('username', length_validator(3))

def run_checks(payload: Dict[str, Any]) -> bool:
    return validator_instance.validate(payload)