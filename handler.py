import json
from typing import Any, Dict, List, Union


def load_json(file_path: str) -> Union[Dict[str, Any], List[Any]]:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f'Error loading JSON: {e}')
        return {}


def save_json(file_path: str, data: Union[Dict[str, Any], List[Any]]) -> None:
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f'Error saving JSON: {e}')


def update_json(file_path: str, updates: Dict[str, Any]) -> None:
    data = load_json(file_path)
    data.update(updates)
    save_json(file_path, data)


def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    items = []
    for k, v in d.items():
        new_key = f'{parent_key}{sep}{k}' if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    merged = {}
    for dictionary in dicts:
        merged.update(dictionary)
    return merged
