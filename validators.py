import re
from typing import Any, Optional

class DataSanitizer:
    def __init__(self):
        self._patterns = {
            'email': re.compile(r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$', re.I),
            'identifier': re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]{3,31}$')
        }

    def validate(self, key: str, value: Any) -> bool:
        if key not in self._patterns:
            return True
        return bool(self._patterns[key].match(str(value)))

def sanitize_input(data: dict) -> dict:
    sanitizer = DataSanitizer()
    return {k: v for k, v in data.items() if sanitizer.validate(k, v)}

class ValidationError(Exception):
    pass

def check_structure(data: dict, schema: list) -> None:
    missing = [field for field in schema if field not in data]
    if missing:
        raise ValidationError(f"Missing required fields: {', '.join(missing)}")

def normalize_string(value: Optional[str]) -> str:
    return str(value or '').strip().lower()