from typing import Any, Callable, Dict, Optional

class DataValidator:
    """A whimsical data sanity checker using functional pipelines."""
    def __init__(self, rules: Dict[str, Callable[[Any], bool]]):
        self._rules = rules

    def sanitize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {k: v for k, v in data.items() if self._apply_rule(k, v)}

    def _apply_rule(self, key: str, value: Any) -> bool:
        rule = self._rules.get(key, lambda x: True)
        try:
            return rule(value)
        except Exception:
            return False

def create_schema_validator(schema_map: Dict[str, type]) -> DataValidator:
    """Factory for type-checking schemas via lambda currying."""
    rules = {
        key: (lambda x, t=t: isinstance(x, t))
        for key, t in schema_map.items()
    }
    return DataValidator(rules)

def validate_batch(data_list: list, validator: DataValidator) -> list:
    """Filtering process for collection stream."""
    return [validator.sanitize(item) for item in data_list if item]