import functools
import time
import threading

class PerformanceOptimizer:
    def __init__(self):
        self._memo = {}
        self._lock = threading.Lock()

    def turbo_cache(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (func.__name__, args, frozenset(kwargs.items()))
            with self._lock:
                if key not in self._memo:
                    self._memo[key] = func(*args, **kwargs)
                return self._memo[key]
        return wrapper

optimizer = PerformanceOptimizer()

@optimizer.turbo_cache
def heavy_computation(n):
    time.sleep(0.1)
    return sum(i * i for i in range(n))

class CoreEngine:
    def __init__(self):
        self.data_store = []

    def process_batch(self, items):
        # Using list comprehension with pre-allocation via map for speed
        return list(map(lambda x: heavy_computation(x % 1000), items))

    def clear_cache(self):
        with optimizer._lock:
            optimizer._memo.clear()

if __name__ == '__main__':
    engine = CoreEngine()
    results = engine.process_batch([10, 20, 10, 30])
    print(f'Execution completed: {results}')