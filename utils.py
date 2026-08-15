import json

class CustomError(Exception):
    pass


def load_json_file(filepath):
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        raise CustomError(f'File {filepath} not found')
    except json.JSONDecodeError:
        raise CustomError(f'Error decoding JSON from file {filepath}')
    except Exception as e:
        raise CustomError(f'Unexpected error: {str(e)}')


def save_json_file(filepath, data):
    try:
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)
    except IOError:
        raise CustomError(f'Error writing to file {filepath}')
    except Exception as e:
        raise CustomError(f'Unexpected error: {str(e)}')


def get_dict_value(d, key):
    try:
        return d[key]
    except KeyError:
        raise CustomError(f'Key {key} not found in dictionary')
    except TypeError:
        raise CustomError('Provided argument is not a dictionary')
    except Exception as e:
        raise CustomError(f'Unexpected error: {str(e)}')