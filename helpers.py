import json
import logging
from typing import Any, Dict, Union

class CustomError(Exception):
    pass

def safe_json_loads(data: str) -> Union[Dict[str, Any], None]:
    try:
        return json.loads(data)
    except json.JSONDecodeError as e:
        logging.error(f'JSON decoding error: {e}')
        return None
    except Exception as e:
        logging.error(f'Unexpected error during JSON parsing: {e}')
        return None

def divide_numbers(numerator: float, denominator: float) -> float:
    try:
        if denominator == 0:
            raise CustomError('Denominator cannot be zero.')
        return numerator / denominator
    except CustomError as e:
        logging.error(e)
        return float('inf')  # Return infinity on error
    except Exception as e:
        logging.error(f'Unexpected error during division: {e}')
        return float('inf')

def safe_get(data: Dict[str, Any], key: str, default: Any = None) -> Any:
    try:
        return data.get(key, default)
    except Exception as e:
        logging.error(f'Error accessing key {key}: {e}')
        return default

