import functools
from typing import Any, Callable, Iterable, TypeVar

T = TypeVar('T')

def pipeline(data: T, *funcs: Callable[[T], T]) -> T:
    """Chain data through a sequence of transformations."""
    return functools.reduce(lambda acc, f: f(acc), funcs, data)

def pluck(key: str) -> Callable[[dict], Any]:
    """Functional extractor for dictionary access."""
    return lambda d: d.get(key)

def batch(iterable: Iterable[T], n: int) -> Iterable[list[T]]:
    """Chunking logic for massive datasets."""
    batch_list = []
    for item in iterable:
        batch_list.append(item)
        if len(batch_list) == n:
            yield batch_list
            batch_list = []
    if batch_list:
        yield batch_list

def clean_data(raw: list[dict], target_key: str) -> list[Any]:
    """Extraction pipeline for specific object keys."""
    return [pipeline(item, pluck(target_key)) for item in raw if item.get(target_key) is not None]

class DataStream:
    def __init__(self, items: Iterable[Any]):
        self.items = items

    def __or__(self, func: Callable[[Iterable], Any]):
        return func(self.items)

    @staticmethod
    def transform(func: Callable[[T], T]):
        return lambda iterable: map(func, iterable)

    @staticmethod
    def collect(iterable: Iterable[T]) -> list[T]:
        return list(iterable)