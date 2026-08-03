import json

def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def write_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def flatten_list(nested_list):
    return [item for sublist in nested_list for item in sublist]


def generate_range(start, end):
    return list(range(start, end + 1))


def merge_dictionaries(dict1, dict2):
    merged = dict1.copy()
    merged.update(dict2)
    return merged


def extract_keys(source_dict, keys):
    return {key: source_dict[key] for key in keys if key in source_dict}