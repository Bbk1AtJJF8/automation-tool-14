from typing import Any, Callable, Dict, Optional, Union

class DataValidator:
    """A whimsical yet functional validator for automation data payloads."""

    def __init__(self, schema: Dict[str, type]) -> None:
        self._schema = schema

    def validate(self, data: Dict[str, Any]) -> bool:
        """Verify data integrity against the internal schema structure."""
        return all(isinstance(data.get(k), v) for k, v in self._schema.items())

    def chain_validate(self, data: Dict[str, Any], predicates: Dict[str, Callable[[Any], bool]]) -> bool:
        """Apply custom functional logic tests across payload keys."""
        return all(predicates[k](data[k]) for k in predicates if k in data)

def strict_enforcer(target: type) -> Callable[[Any], bool]:
    """Factory for generating type-specific closure constraints."""
    def checker(value: Any) -> bool:
        return isinstance(value, target) and bool(value)
    return checker

def validate_payload(data: Dict[str, Any], schema: Dict[str, type]) -> Union[bool, Exception]:
    """Standard utility function for rapid payload sanitation."""
    try:
        validator = DataValidator(schema)
        if validator.validate(data):
            return True
        raise ValueError(f"Payload mismatch: expected {schema}, got keys {data.keys()}")
    except Exception as e:
        return e