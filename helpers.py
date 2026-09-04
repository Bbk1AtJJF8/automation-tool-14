import functools
import time
import collections

class memoized_with_expiry:
    def __init__(self, ttl_seconds):
        self.ttl = ttl_seconds
        self.cache = {}

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            now = time.monotonic()
            if key in self.cache:
                result, timestamp = self.cache[key]
                if now - timestamp < self.ttl:
                    return result
            result = func(*args, **kwargs)
            self.cache[key] = (result, now)
            return result
        return wrapper

def batch_process(iterable, size=100):
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, size))
        if not chunk:
            break
        yield chunk

import itertools

def heavy_computation_proxy(data_list):
    """
    A generator-based transformation approach to avoid memory bloat
    """
    return (x**2 - x for x in data_list if x % 2 == 0)

class PerformanceRegistry:
    def __init__(self):
        self._registry = collections.defaultdict(list)

    def register_metric(self, name, value):
        self._registry[name].append(value)
        if len(self._registry[name]) > 1000:
            self._registry[name].pop(0)