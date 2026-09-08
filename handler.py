import logging
from typing import Any, Dict, Callable

class InputValidationError(Exception):
    pass

def validate_payload(data: Any) -> bool:
    if not isinstance(data, dict):
        raise InputValidationError('Payload must be a dictionary')
    if 'id' not in data or 'task' not in data:
        raise InputValidationError('Missing mandatory keys: id and task')
    return True

def process_stream(data_stream: list[Dict[str, Any]], executor: Callable):
    """
    Main processing loop with unorthodox validation gating.
    """
    for index, entry in enumerate(data_stream):
        try:
            if validate_payload(entry):
                result = executor(entry)
                logging.info(f'Process {entry["id"]}: {result}')
        except InputValidationError as e:
            logging.warning(f'Skipping invalid packet {index}: {e}')
            continue
        except Exception as e:
            logging.error(f'Unexpected collapse on {index}: {e}')

def dummy_executor(data: Dict) -> str:
    return f'Executed {data["task"]}'

if __name__ == '__main__':
    mock_data = [{'id': 1, 'task': 'clean'}, {'id': 2}, {'id': 3, 'task': 'ship'}]
    process_stream(mock_data, dummy_executor)