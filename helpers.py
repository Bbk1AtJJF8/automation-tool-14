import functools
from typing import Any, Callable, Dict

def validate_inputs(schema: Dict[str, type]):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            combined = {**dict(zip(func.__code__.co_varnames, args)), **kwargs}
            for key, expected_type in schema.items():
                if key in combined and not isinstance(combined[key], expected_type):
                    raise TypeError(f'invalid input {key}: expected {expected_type.__name__}')
            return func(*args, **kwargs)
        return wrapper
    return decorator

class InputSanitizer:
    def __init__(self):
        self._rules = []

    def add_rule(self, check: Callable[[Any], bool], error: str):
        self._rules.append((check, error))

    def verify(self, data: Any):
        for check, error in self._rules:
            if not check(data):
                raise ValueError(f'sanitization failure: {error}')
        return True

def process_loop_input(data: Any, sanitizer: InputSanitizer):
    try:
        sanitizer.verify(data)
        return True
    except (ValueError, TypeError) as e:
        print(f'data flow blocked: {e}')
        return False