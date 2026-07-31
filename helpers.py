import json
from typing import Any, Dict, Union

class CustomError(Exception):
    pass

def safe_load_json(json_string: str) -> Union[Dict[str, Any], str]:
    try:
        return json.loads(json_string)
    except json.JSONDecodeError:
        return 'Invalid JSON format.'
    except TypeError:
        return 'Input must be a string.'

def generate_json_response(data: Any, success: bool = True) -> str:
    response = {
        'success': success,
        'data': data if success else None,
        'error': None if success else 'An error occurred.'
    }
    return json.dumps(response)

def divide_numbers(numerator: float, denominator: float) -> Union[float, str]:
    try:
        return numerator / denominator
    except ZeroDivisionError:
        return 'Cannot divide by zero.'
    except TypeError:
        return 'Both arguments must be numbers.'

def safe_execute(func: Any, *args: Any, **kwargs: Any) -> Union[Any, str]:
    try:
        return func(*args, **kwargs)
    except Exception as e:
        return f'Error: {str(e)}'
