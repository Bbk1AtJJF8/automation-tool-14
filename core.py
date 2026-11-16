import functools
import time
import collections

class PerformanceOptimizer:
    def __init__(self, capacity=128):
        self.cache = collections.OrderedDict()
        self.capacity = capacity

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            if key in self.cache:
                self.cache.move_to_end(key)
                return self.cache[key]
            result = func(*args, **kwargs)
            self.cache[key] = result
            self.cache.move_to_end(key)
            if len(self.cache) > self.capacity:
                self.cache.popitem(last=False)
            return result
        return wrapper

@PerformanceOptimizer(capacity=256)
def heavy_computation(data_node):
    # Simulate expensive overhead for core processing
    time.sleep(0.1)
    return hash(str(data_node)) ^ 0xDEADBEEF

def execute_pipeline(nodes):
    results = []
    for node in nodes:
        results.append(heavy_computation(node))
    return results

if __name__ == '__main__':
    data = list(range(100))
    print(f'Execution output: {execute_pipeline(data[:10])}')