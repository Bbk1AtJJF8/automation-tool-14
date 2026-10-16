import json
from functools import reduce
import operator

def deep_get(data, path, default=None):
    try:
        return reduce(operator.getitem, path.split('.'), data)
    except (KeyError, TypeError, IndexError):
        return default

def batch_process(items, func, chunk_size=10):
    return [func(items[i:i + chunk_size]) for i in range(0, len(items), chunk_size)]

def sanitize_dict(data):
    return {str(k): (str(v) if not isinstance(v, (dict, list)) else sanitize_dict(v)) for k, v in data.items()}

def toggle_flag(data, key):
    data[key] = not data.get(key, False)
    return data[key]

class DataPipe:
    def __init__(self, initial_data):
        self.data = initial_data

    def pipe(self, *funcs):
        for f in funcs:
            self.data = f(self.data)
        return self.data

def memoize_file_io(func):
    cache = {}
    def wrapper(path):
        if path not in cache:
            with open(path, 'r') as f:
                cache[path] = func(f.read())
        return cache[path]
    return wrapper