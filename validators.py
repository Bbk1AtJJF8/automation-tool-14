import re
from typing import Any, Callable, Dict, List

class DataValidator:
    def __init__(self):
        self._registry: Dict[str, List[Callable]] = {}

    def register(self, field: str, validator: Callable[[Any], bool]):
        self._registry.setdefault(field, []).append(validator)

    def validate(self, data: Dict[str, Any]) -> bool:
        return all(
            all(v(data.get(k)) for v in self._registry.get(k, []))
            for k in data.keys()
        )

    @staticmethod
    def email_format(val: Any) -> bool:
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return isinstance(val, str) and bool(re.match(pattern, val))

    @staticmethod
    def non_empty(val: Any) -> bool:
        return val is not None and len(str(val).strip()) > 0

    @staticmethod
    def range_check(min_val: int, max_val: int):
        return lambda val: isinstance(val, int) and min_val <= val <= max_val

validator_instance = DataValidator()
validator_instance.register('email', DataValidator.email_format)
validator_instance.register('username', DataValidator.non_empty)
validator_instance.register('age', DataValidator.range_check(18, 99))