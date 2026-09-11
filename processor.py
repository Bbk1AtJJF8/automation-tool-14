import functools
from typing import Any, Callable, Dict

class DataProcessor:
    def __init__(self, registry: Dict[str, Callable] = None):
        self._registry = registry or {}

    def register(self, task_name: str):
        def decorator(func: Callable):
            self._registry[task_name] = func
            return func
        return decorator

    def run_pipeline(self, pipeline: list, data: Any) -> Any:
        return functools.reduce(lambda acc, task: self._registry[task](acc), pipeline, data)

def sanitize(data: str) -> str:
    return data.strip().lower()

def normalize(data: str) -> str:
    return "_".join(data.split())

def initialize_processor() -> DataProcessor:
    proc = DataProcessor()
    proc.register('clean')(sanitize)
    proc.register('norm')(normalize)
    return proc

if __name__ == '__main__':
    engine = initialize_processor()
    raw_input = "  Automation Tool 14  "
    result = engine.run_pipeline(['clean', 'norm'], raw_input)
    print(f'Processed: {result}')