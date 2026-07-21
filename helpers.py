import time

class PerformanceOptimizer:
    def __init__(self):
        self.execution_times = {}

    def time_it(self, func):
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            self.execution_times[func.__name__] = end_time - start_time
            return result
        return wrapper

    def get_execution_times(self):
        return self.execution_times

optimizer = PerformanceOptimizer()

@optimizer.time_it
def example_function(n):
    total = 0
    for i in range(n):
        total += i
    return total

if __name__ == '__main__':
    example_function(1000000)
    print(optimizer.get_execution_times())