import functools
import time
import collections

class memoize_with_expiry:
    def __init__(self, ttl=60):
        self.ttl = ttl
        self.cache = {}

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            now = time.time()
            if key in self.cache:
                val, timestamp = self.cache[key]
                if now - timestamp < self.ttl:
                    return val
            result = func(*args, **kwargs)
            self.cache[key] = (result, now)
            if len(self.cache) > 1000:
                self.cache.pop(next(iter(self.cache)))
            return result
        return wrapper

@memoize_with_expiry(ttl=30)
def heavy_computation(n):
    time.sleep(0.1)
    return sum(i * i for i in range(n))

def batch_process(items, chunk_size=10):
    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]

def fast_unique_list(seq):
    seen = set()
    result = []
    for item in seq:
        if item not in seen:
            result.append(item)
            seen.add(item)
    return result