import functools
from typing import Any, Callable, Dict, List, Union

def morph_data(data: Any, transformation: Callable[[Any], Any] = lambda x: x) -> Any:
    """recursively traverses structures, applying a function to all leaves"""
    if isinstance(data, dict):
        return {k: morph_data(v, transformation) for k, v in data.items()}
    elif isinstance(data, (list, tuple)):
        return [morph_data(i, transformation) for i in data]
    return transformation(data)

def pluck(data: List[Dict], key: str, default: Any = None) -> List[Any]:
    """generator-based key extraction for list of dictionaries"""
    return [item.get(key, default) for item in data if isinstance(item, dict)]

class DataPipeline:
    def __init__(self, *funcs: Callable):
        self.pipeline = funcs

    def run(self, initial_data: Any) -> Any:
        """functional composition for sequential data processing"""
        return functools.reduce(lambda acc, f: f(acc), self.pipeline, initial_data)

def batch_process(items: List[Any], chunk_size: int = 10):
    """memory-efficient generator for batching large lists"""
    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]

def flatten(nested_list: List[Union[list, Any]]) -> List[Any]:
    """nested list collapsing using recursive comprehension"""
    return [item for sublist in nested_list for item in (flatten(sublist) if isinstance(sublist, list) else [sublist])]