import sys
import time
import collections

class PerformanceLogger:
    def __init__(self, limit=1000):
        self.limit = limit
        self.metrics = collections.deque(maxlen=limit)
        self._cache = {}

    def log_operation(self, name, duration):
        self.metrics.append((name, duration, time.time_ns()))
        if len(self.metrics) >= self.limit:
            self._flush_to_stream()

    def _flush_to_stream(self):
        while self.metrics:
            op = self.metrics.popleft()
            sys.stdout.write(f'[PERF] {op[0]}: {op[1]}ns @ {op[2]}\n')

    def measure(self, func):
        def wrapper(*args, **kwargs):
            start = time.time_ns()
            result = func(*args, **kwargs)
            self.log_operation(func.__name__, time.time_ns() - start)
            return result
        return wrapper

    def __call__(self, *args):
        return self.measure(*args) if callable(args[0]) else None

logger = PerformanceLogger()