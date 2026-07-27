import time
from functools import wraps

class PerformanceOptimizer:
    def __init__(self):
        self.execution_times = []

    def log_time(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            self.execution_times.append(end_time - start_time)
            return result
        return wrapper

    def average_time(self):
        if not self.execution_times:
            return 0
        return sum(self.execution_times) / len(self.execution_times)

performance_optimizer = PerformanceOptimizer()

@performance_optimizer.log_time
def sample_function(x):
    time.sleep(x)
    return x ** 2

for i in range(1, 4):
    print(sample_function(i))

print(f"Average execution time: {performance_optimizer.average_time()} seconds")