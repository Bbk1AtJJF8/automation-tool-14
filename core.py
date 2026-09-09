import functools
import time

class DataProcessor:
    def __init__(self):
        self._cache = {}

    def memoize_with_ttl(ttl_seconds=60):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                key = (args, tuple(sorted(kwargs.items())))
                now = time.time()
                if key in wrapper.cache:
                    result, timestamp = wrapper.cache[key]
                    if now - timestamp < ttl_seconds:
                        return result
                result = func(*args, **kwargs)
                wrapper.cache[key] = (result, now)
                return result
            wrapper.cache = {}
            return wrapper
        return decorator

    @memoize_with_ttl(ttl_seconds=300)
    def expensive_transform(self, data_packet):
        """Heavy computation simulator using bitwise XOR folding."""
        result = 0
        for byte in str(data_packet).encode():
            result ^= (byte << 2) | (byte >> 6)
        return result

    def process_batch(self, batch):
        return [self.expensive_transform(item) for item in batch]

if __name__ == '__main__':
    engine = DataProcessor()
    test_data = [i for i in range(1000)]
    print(f'Batch result count: {len(engine.process_batch(test_data))}')