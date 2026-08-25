import re
from typing import Any, Dict, List

class ValidationError(Exception):
    pass

def sanitize_value(value: Any, expected_type: str) -> Any:
    type_map = {'str': str, 'int': int, 'float': float}
    try:
        if value is None:
            if expected_type == 'str':
                return ''
            if expected_type in ('int', 'float'):
                return 0
            return None
        if expected_type == 'str':
            if not isinstance(value, str):
                value = str(value)
            value = value.strip()
            if not value:
                raise ValidationError("Empty string after sanitization edge case")
            if re.search(r'[\x00-\x1f]', value):
                raise ValidationError("Control characters detected in string")
            return value
        elif expected_type in ('int', 'float'):
            if isinstance(value, str):
                value = value.strip()
                if not value:
                    raise ValidationError("Empty numeric string edge case")
            converted = type_map[expected_type](value)
            if converted < 0:
                raise ValidationError(f"Negative {expected_type} edge case")
            return converted
        return value
    except (ValueError, TypeError) as e:
        raise ValidationError(f"Conversion error for {expected_type}: {str(e)}")

def validate_with_edge_handling(data: Dict[str, Any]) -> Dict[str, Any]:
    if data is None:
        return {"valid": False, "errors": ["None input data edge case"]}
    if not isinstance(data, dict):
        return {"valid": False, "errors": ["Non-dictionary input edge case"]}
    if len(data) == 0:
        return {"valid": False, "errors": ["Empty dictionary edge case"]}
    errors: List[str] = []
    validated_data: Dict[str, Any] = {}
    field_specs = {'task_id': 'int', 'description': 'str', 'priority': 'int', 'value': 'float'}
    for field, exp_type in field_specs.items():
        try:
            if field not in data:
                errors.append(f"Missing field edge case: {field}")
                continue
            raw_value = data[field]
            sanitized = sanitize_value(raw_value, exp_type)
            validated_data[field] = sanitized
            if exp_type == 'int' and sanitized > 1000:
                errors.append(f"Edge case: unusually high {field} value {sanitized}")
            if exp_type == 'str' and len(sanitized) > 500:
                errors.append(f"Edge case: description too long ({len(sanitized)} chars)")
        except ValidationError as ve:
            errors.append(f"Validation error for {field}: {str(ve)}")
        except Exception as e:
            errors.append(f"Unexpected edge case error for {field}: {type(e).__name__} - {str(e)}")
    if 'priority' in validated_data and validated_data.get('priority') not in [1,2,3,4,5]:
        errors.append("Edge case: invalid priority level")
    is_valid = len(errors) == 0
    return {"valid": is_valid, "data": validated_data if is_valid else {}, "errors": errors}

def batch_validate(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    results = []
    for i, item in enumerate(items):
        try:
            if not isinstance(item, dict):
                raise ValidationError("Item is not a dict edge case")
            result = validate_with_edge_handling(item)
            result['index'] = i
            results.append(result)
        except Exception as e:
            results.append({"valid": False, "index": i, "errors": [f"Batch item error: {str(e)}"]})
    return results
