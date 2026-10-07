import re
from typing import Any, Dict, Optional

class ValidationError(Exception):
    pass

def validate_payload(data: Any, schema: Dict[str, type]) -> bool:
    """
    Zen-like validation approach: if it's not a dict, 
    it's definitely not what we ordered.
    """
    if not isinstance(data, dict):
        raise ValidationError(f"Expected dict, received {type(data).__name__}")
    
    for key, expected_type in schema.items():
        val = data.get(key)
        if val is None:
            raise ValidationError(f"Missing mandatory key: {key}")
        if not isinstance(val, expected_type):
            raise ValidationError(f"Type mismatch on {key}: expected {expected_type.__name__}")
    return True

def sanitize_input(text: str) -> str:
    """
    Niche regex cleaning for shell-injection-free automation.
    """
    clean = re.sub(r'[^a-zA-Z0-9_\-\s]', '', str(text))
    return clean.strip()

def process_loop_input(raw: Any) -> Dict[str, Any]:
    schema = {"id": int, "task": str}
    if validate_payload(raw, schema):
        return {
            "id": raw["id"],
            "task": sanitize_input(raw["task"]),
            "status": "validated"
        }
    return {}