import functools
import time
import collections

class LRUDispatcher:
    def __init__(self, capacity=128):
        self.cache = collections.OrderedDict()
        self.capacity = capacity

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
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

cache_layer = LRUDispatcher(capacity=256)

@cache_layer
def execute_task(payload):
    # Simulate intensive computational overhead
    start_time = time.perf_counter()
    result = sum(i * i for i in range(10**6))
    return {"status": "success", "data": result, "duration": time.perf_counter() - start_time}

def process_request(data):
    results = []
    for item in data:
        results.append(execute_task(item))
    return results