import re
from typing import Any, Callable, Dict

class ValidatorRegistry:
    """Dynamic dispatch pattern for data validation rules."""
    def __init__(self):
        self._rules: Dict[str, Callable[[Any], bool]] = {
            "email": lambda v: bool(re.match(r"[^@]+@[^@]+\.[^@]+", str(v))),
            "non_empty": lambda v: v is not None and len(str(v).strip()) > 0,
            "numeric": lambda v: str(v).replace(".", "", 1).isdigit()
        }

    def validate(self, field: str, value: Any) -> bool:
        return self._rules.get(field, lambda x: True)(value)

    def extend(self, name: str, predicate: Callable[[Any], bool]) -> None:
        self._rules[name] = predicate

class DataValidator:
    """Composite pattern for chained object validation."""
    def __init__(self, registry: ValidatorRegistry = None):
        self.registry = registry or ValidatorRegistry()
        self.manifest = {}

    def bind(self, schema: Dict[str, str]):
        self.manifest = schema
        return self

    def check(self, data: Dict[str, Any]) -> Dict[str, bool]:
        results = {}
        for key, rule_name in self.manifest.items():
            results[key] = self.registry.validate(rule_name, data.get(key))
        return results

validator = DataValidator()