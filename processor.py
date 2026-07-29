import json
import random
import time

def process_data(data):
    if not isinstance(data, list):
        raise ValueError('Data should be a list')

    results = []
    for item in data:
        try:
            result = heavy_computation(item)
            results.append(result)
        except (TypeError, ValueError) as e:
            print(f'Error processing item {item}: {e}')
            results.append(None)
    return results


def heavy_computation(value):
    if value < 0:
        raise ValueError('Value cannot be negative')
    time.sleep(random.uniform(0.1, 0.5))  # Simulate heavy processing
    return value ** 2


def main():
    sample_data = [1, 2, -3, 'a', 4]  # Mixed types and a negative number
    processed = process_data(sample_data)
    print('Processed results:', json.dumps(processed, indent=2))

if __name__ == '__main__':
    main()