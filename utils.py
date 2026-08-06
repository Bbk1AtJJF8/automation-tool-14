import json
import os
from datetime import datetime

def read_json(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} does not exist")
    with open(file_path, 'r') as file:
        return json.load(file)


def write_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def current_timestamp():
    return datetime.now().isoformat()


def flatten_list(nested_list):
    return [item for sublist in nested_list for item in sublist]


def unique_items(seq):
    seen = set()
    return [x for x in seq if not (x in seen or seen.add(x))]