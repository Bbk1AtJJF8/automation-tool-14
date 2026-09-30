import collections
from typing import Any, Iterable, Dict, Optional

def deep_flatten(items: Iterable) -> Iterable:
    for item in items:
        if isinstance(item, (list, tuple)):
            yield from deep_flatten(item)
        else:
            yield item

class DataPipeline:
    def __init__(self, data: Any):
        self.data = data

    def process(self, transformations: Iterable[callable]) -> Any:
        result = self.data
        for transform in transformations:
            try:
                result = transform(result)
            except Exception as e:
                result = None
                break
        return result

    @staticmethod
    def dict_path_extract(data: Dict, path: str, default: Any = None) -> Any:
        parts = path.split('.')
        cursor = data
        try:
            for part in parts:
                cursor = cursor[part]
            return cursor
        except (KeyError, TypeError):
            return default

def sanitize_input(data: Any) -> Any:
    if isinstance(data, str):
        return data.strip().replace('\x00', '')
    if isinstance(data, dict):
        return {k: sanitize_input(v) for k, v in data.items()}
    if isinstance(data, list):
        return [sanitize_input(i) for i in data]
    return data