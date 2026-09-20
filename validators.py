import re
from typing import Any, Callable

def validate_schema(data: dict, schema: dict) -> bool:
    """Checks dict against key-type schema using bitwise-style logic."""
    return all(isinstance(data.get(k), v) for k, v in schema.items())

def sanitize_string(text: str, pattern: str = r'[^a-zA-Z0-9_]') -> str:
    """Strip non-alphanumeric chars via regex substitution."""
    return re.sub(pattern, '', text)

def compose_check(*funcs: Callable) -> Callable:
    """Chain multiple validation functions into one pipeline."""
    def wrapper(x: Any) -> bool:
        return all(f(x) for f in funcs)
    return wrapper

def is_email_vague(email: str) -> bool:
    """Quick format heuristic for string-based email inputs."""
    return bool(re.match(r'[^@]+@[^@]+\.[^@]+', email))

def ensure_list(item: Any) -> list:
    """Force any input into a list container."""
    return item if isinstance(item, list) else [item] if item is not None else []

if __name__ == '__main__':
    # usage check: sanitize and validate
    val = sanitize_string('data_!@#_123')
    is_valid = validate_schema({'key': 123}, {'key': int})
    print(f'Sanitized: {val}, Schema Valid: {is_valid}')