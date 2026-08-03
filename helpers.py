import re

def validate_input(data):
    if not isinstance(data, dict):
        raise ValueError('Input must be a dictionary')
    for key, value in data.items():
        if not isinstance(key, str):
            raise ValueError('Keys must be strings')
        if not isinstance(value, (int, float, str)):
            raise ValueError('Values must be int, float or str')
        if isinstance(value, str) and not re.match('^[a-zA-Z0-9_]+$', value):
            raise ValueError('String values must be alphanumeric')

if __name__ == '__main__':
    sample_data = {'name': 'JohnDoe', 'age': 30, 'score': 88.5}
    try:
        validate_input(sample_data)
        print('Input is valid')
    except ValueError as e:
        print(f'Error: {e}')