import sys
from typing import Any, Callable, Generator, Dict, List, Union


class ValidationError(Exception):
    def __init__(self, key: str, reason: str):
        self.key = key
        self.reason = reason
        super().__init__(f"Invalid payload at '{key}': {reason}")


def payload_validator(schema: Dict[str, type]) -> Callable:
    def validate(item: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(item, dict):
            raise ValidationError("root", "item must be a dictionary")
        for key, expected_type in schema.items():
            if key not in item:
                raise ValidationError(key, "missing required field")
            if not isinstance(item[key], expected_type):
                actual = type(item[key]).__name__
                raise ValidationError(key, f"expected {expected_type.__name__}, got {actual}")
            if isinstance(item[key], (int, float)) and item[key] < 0:
                raise ValidationError(key, "numeric values must be non-negative")
        return item
    return validate


def process_stream(
    raw_stream: List[Any],
    schema: Dict[str, type]
) -> Generator[Dict[str, Any], None, None]:
    validator = payload_validator(schema)
    
    for idx, raw_input in enumerate(raw_stream):
        try:
            match raw_input:
                case {"status": "skip"}:
                    continue
                case {"payload": dict() as payload}:
                    validated_data = validator(payload)
                    validated_data["_processed_index"] = idx
                    yield validated_data
                case _:
                    raise ValidationError("envelope", f"malformed structure at index {idx}")
        except ValidationError as err:
            yield {"_error": str(err), "_raw": raw_input, "_processed_index": idx}


if __name__ == "__main__":
    test_schema = {"id": int, "name": str, "score": float}
    stream = [
        {"payload": {"id": 101, "name": "alpha", "score": 98.5}},
        {"status": "skip"},
        {"payload": {"id": "102", "name": "beta", "score": 45.0}},
        {"payload": {"id": 103, "name": "gamma", "score": -5.0}},
        "invalid_envelope_format",
    ]
    
    for result in process_stream(stream, test_schema):
        sys.stdout.write(f"{result}\n")