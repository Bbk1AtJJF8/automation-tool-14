import json
from collections import defaultdict
from typing import Any, Dict, List, Union

def flatten_dict(nested_dict: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    items = []
    for key, value in nested_dict.items():
        new_key = f'{parent_key}{sep}{key}' if parent_key else key
        if isinstance(value, dict):
            items.extend(flatten_dict(value, new_key, sep=sep).items())
        else:
            items.append((new_key, value))
    return dict(items)


def merge_dicts(dicts: List[Dict[str, Any]]) -> Dict[str, Any]:
    merged = defaultdict(list)
    for d in dicts:
        for key, value in d.items():
            merged[key].append(value)
    return {k: v if len(v) > 1 else v[0] for k, v in merged.items()}


def save_to_json(data: Union[Dict, List], filename: str) -> None:
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def load_from_json(filename: str) -> Union[Dict, List]:
    with open(filename, 'r') as json_file:
        return json.load(json_file)