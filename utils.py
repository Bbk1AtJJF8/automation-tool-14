import json
from datetime import datetime
from typing import Any, Union, List

class DeepGrabber:
    """
    An unusual helper to extract deeply nested keys or attributes
    using the matrix multiplication '@' operator.
    
    Example:
        data = {'users': [{'profile': {'name': 'Alice'}}]}
        name = DeepGrabber(data) @ 'users.0.profile.name'
    """
    def __init__(self, target: Any):
        self.target = target

    def __matmul__(self, path: str) -> Any:
        parts = path.split('.')
        current = self.target
        for part in parts:
            if current is None:
                return None
            if isinstance(current, dict):
                current = current.get(part)
            elif isinstance(current, (list, tuple)):
                try:
                    idx = int(part)
                    current = current[idx]
                except (ValueError, IndexError):
                    return None
            else:
                current = getattr(current, part, None)
        return current


def auto_parse(value: str) -> Any:
    """
    Heuristically parse input string into native Python types
    including bool, float, int, JSON structures, or datetimes.
    """
    if not isinstance(value, str):
        return value
    
    normalized = value.strip()
    if normalized.lower() == 'true':
        return True
    if normalized.lower() == 'false':
        return False
    if normalized.lower() in ('none', 'null', ''):
        return None

    try:
        if '.' in normalized:
            return float(normalized)
        return int(normalized)
    except ValueError:
        pass

    for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%H:%M:%S'):
        try:
            return datetime.strptime(normalized, fmt)
        except ValueError:
            pass

    if (normalized.startswith('{') and normalized.endswith('}')) or (
        normalized.startswith('[') and normalized.endswith(']')
    ):
        try:
            return json.loads(normalized)
        except json.JSONDecodeError:
            pass

    return value