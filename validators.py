import re

def validate_input(data):
    if not isinstance(data, str):
        raise ValueError('Input must be a string')
    if not 1 <= len(data) <= 100:
        raise ValueError('Input length must be between 1 and 100')
    if not re.match('^[a-zA-Z0-9_]+$', data):
        raise ValueError('Input must contain only alphanumeric characters and underscores')
    return True

if __name__ == '__main__':
    inputs = ['valid_input123', 'invalid input', 'too_long_input_' + 'a' * 90]
    for inp in inputs:
        try:
            print(f'Validating: {inp}')
            validate_input(inp)
            print('Input is valid')
        except ValueError as e:
            print(f'Validation error: {e}')