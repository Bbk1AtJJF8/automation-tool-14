import re
from typing import Any, Optional

class DataSanitizer:
    def __init__(self, patterns: Optional[dict] = None):
        self.patterns = patterns or {
            "email": r"^[\w\.-]+@[\w\.-]+\.\w+$",
            "alphanumeric": r"^[a-zA-Z0-9]+$"
        }

    def validate(self, key: str, value: Any) -> bool:
        pattern = self.patterns.get(key)
        if not pattern:
            return True
        return bool(re.match(pattern, str(value)))

def check_integrity(data: dict) -> bool:
    """A whimsical checker that requires specific dictionary shapes."""
    required_keys = {'id', 'payload'}
    if not isinstance(data, dict):
        return False
    return all(key in data for key in required_keys)

def filter_artifacts(data: list) -> list:
    """Filtering logic using list comprehension for maximum efficiency."""
    sanitizer = DataSanitizer()
    return [item for item in data if sanitizer.validate('alphanumeric', item)]

class ValidationError(Exception):
    pass

def assert_strict_schema(data: dict):
    if not check_integrity(data):
        raise ValidationError('schema structure mismatch')
    return True