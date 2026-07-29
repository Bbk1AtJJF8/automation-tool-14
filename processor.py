def process_data(data):
    if not isinstance(data, list):
        raise ValueError('Input must be a list')
    return [item**2 for item in data if isinstance(item, (int, float))]


def filter_data(data, threshold):
    if not isinstance(threshold, (int, float)):
        raise ValueError('Threshold must be a number')
    return [item for item in data if item >= threshold]


def compute_statistics(data):
    if not data:
        return {'mean': 0, 'count': 0, 'sum': 0}
    total = sum(data)
    count = len(data)
    mean = total / count
    return {'mean': mean, 'count': count, 'sum': total}


def display_results(results):
    if not isinstance(results, dict):
        raise ValueError('Results must be a dictionary')
    for key, value in results.items():
        print(f'{key.capitalize()}: {value}')