import functools
import logging
from typing import Callable, Any

class DataProcessor:
    def __init__(self, mode: str = 'strict'):
        self.mode = mode
        self.log = logging.getLogger('automation-tool-14')

    def pipeline(self, *funcs: Callable) -> Callable:
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                result = func(*args, **kwargs)
                for f in funcs:
                    result = f(result)
                return result
            return wrapper
        return decorator

    def sanitize(self, data: str) -> str:
        return data.strip().lower()

    def validate(self, data: Any) -> Any:
        if self.mode == 'strict' and not data:
            raise ValueError('empty payload detected')
        return data

def execute_task(raw_input: str) -> str:
    p = DataProcessor(mode='loose')
    
    @p.pipeline(p.sanitize, p.validate)
    def process(val: str) -> str:
        return val
    
    return process(raw_input)

if __name__ == '__main__':
    print(execute_task('  AUTOMATION_SUCCESS  '))