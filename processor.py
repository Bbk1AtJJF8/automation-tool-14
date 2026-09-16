import functools
import time
import uuid
from typing import Callable, Any

def with_telemetry(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f'[METRIC] {func.__name__} executed in {time.perf_counter() - start:.4f}s')
        return result
    return wrapper

def generate_id(prefix: str = 'task') -> str:
    return f'{prefix}_{uuid.uuid4().hex[:8]}'

def batch_process(items: list, chunk_size: int = 10):
    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]

class DataPipeline:
    def __init__(self):
        self.registry = {}

    def register_hook(self, name: str):
        def decorator(func: Callable):
            self.registry[name] = func
            return func
        return decorator

    def execute(self, name: str, *args, **kwargs):
        if name in self.registry:
            return self.registry[name](*args, **kwargs)
        raise ValueError(f'Hook {name} not found')

@with_telemetry
def transform_data(data: list) -> list:
    return [d * 2 for d in data if isinstance(d, int)]

def safe_get(data: dict, keys: str, default: Any = None) -> Any:
    return functools.reduce(lambda d, k: d.get(k, {}) if isinstance(d, dict) else default, keys.split('.'), data) or default