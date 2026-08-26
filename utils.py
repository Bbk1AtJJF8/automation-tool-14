import os
import sys
import time
from functools import wraps

def flatten_dict(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def retry(retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    if attempt == retries:
                        raise e
                    time.sleep(delay * attempt)
        return wrapper
    return decorator

@retry(retries=2, delay=0.1)
def safe_file_read(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Target {filepath} is missing")
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

class DictAttrNamespace:
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                setattr(self, key, DictAttrNamespace(value))
            else:
                setattr(self, key, value)
