import functools
import time

class MemoizeWithExpiry:
    def __init__(self, ttl=60):
        self.ttl = ttl
        self.cache = {}

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            now = time.time()
            if key in self.cache:
                result, timestamp = self.cache[key]
                if now - timestamp < self.ttl:
                    return result
            result = func(*args, **kwargs)
            self.cache[key] = (result, now)
            return result
        return wrapper

class PerformanceOptimizer:
    def __init__(self, limit=1000):
        self.registry = {}
        self.limit = limit

    def batch_process(self, data, func):
        if len(data) > self.limit:
            return self._optimized_chunking(data, func)
        return [func(item) for item in data]

    def _optimized_chunking(self, data, func):
        results = []
        for i in range(0, len(data), self.limit):
            chunk = data[i:i + self.limit]
            results.extend(map(func, chunk))
        return results

core_optimizer = PerformanceOptimizer()