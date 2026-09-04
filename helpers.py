import functools
from typing import Any, Callable, Dict

def validate_payload(schema: Dict[str, type]):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data = args[0] if args else kwargs.get('data')
            if not isinstance(data, dict):
                raise ValueError(f"payload must be dict, got {type(data).__name__}")
            for key, expected_type in schema.items():
                if key not in data:
                    raise KeyError(f"missing required field: {key}")
                if not isinstance(data[key], expected_type):
                    raise TypeError(f"field {key} expects {expected_type}, got {type(data[key])}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def process_stream(items: list, validator: Callable):
    processed = []
    for item in items:
        try:
            processed.append(validator(item))
        except (ValueError, TypeError, KeyError) as e:
            print(f"skip item due to {type(e).__name__}: {e}")
    return processed

@validate_payload({'id': int, 'task': str})
def run_task(data: dict):
    return f"executing {data['task']} (ID: {data['id']})"