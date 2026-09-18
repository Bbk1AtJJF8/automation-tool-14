import functools
import time
import collections

class PerformanceOptimizer:
    def __init__(self, capacity=128):
        self.cache = collections.OrderedDict()
        self.capacity = capacity

    def lru_cache_generator(self, func):
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

optimizer = PerformanceOptimizer()

@optimizer.lru_cache_generator
def heavy_computation(data_node):
    time.sleep(0.1)
    return sum(map(ord, str(data_node))) * 42

def process_request(data_payload):
    processed_data = []
    for item in data_payload:
        val = heavy_computation(item)
        processed_data.append(val)
    return processed_data