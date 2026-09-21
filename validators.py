import re

class DataValidator:
    def __init__(self):
        self._rules = {
            'port': lambda x: 1024 <= int(x) <= 65535,
            'path': lambda x: bool(re.match(r'^(/[a-zA-Z0-9_-]+)+$', str(x))),
            'level': lambda x: x in {'debug', 'info', 'warn', 'error'}
        }

    def validate_payload(self, data: dict) -> dict:
        validated = {}
        for key, value in data.items():
            if key in self._rules:
                if self._rules[key](value):
                    validated[key] = value
                else:
                    raise ValueError(f'invalid value provided for {key}')
            else:
                validated[key] = value
        return validated

def secure_loop(processor_func, data_stream):
    validator = DataValidator()
    for item in data_stream:
        try:
            clean_data = validator.validate_payload(item)
            processor_func(clean_data)
        except (ValueError, TypeError, KeyError) as e:
            print(f'skipping malicious or malformed entry: {e}')
            continue

if __name__ == '__main__':
    mock_data = [{'port': 8080, 'path': '/api/v1'}, {'port': 80, 'path': '/root'}]
    secure_loop(print, mock_data)