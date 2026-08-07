import time
from functools import lru_cache

@lru_cache(maxsize=128)
def compute_heavy_operation(data):
    time.sleep(2)  # Simulate a heavy computation
    return sum(data)

class DataProcessor:
    def __init__(self, data):
        self.data = data

    def process_data(self):
        results = []
        for chunk in self.data:
            result = compute_heavy_operation(tuple(chunk))
            results.append(result)
        return results

if __name__ == '__main__':
    data_chunks = [range(1000), range(1000)] * 5  # Sample data
    processor = DataProcessor(data_chunks)
    start_time = time.time()
    results = processor.process_data()
    end_time = time.time()
    print(f'Processed results: {results}')
    print(f'Time taken: {end_time - start_time} seconds')