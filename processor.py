def process_data(data):
    if not isinstance(data, list):
        raise ValueError("Input should be a list")
    return [x * 2 for x in data if isinstance(x, (int, float))]


def sort_data(data):
    if not isinstance(data, list):
        raise ValueError("Input should be a list")
    return sorted(data)


def filter_even(data):
    if not isinstance(data, list):
        raise ValueError("Input should be a list")
    return [x for x in data if isinstance(x, int) and x % 2 == 0]


def aggregate_data(data):
    if not isinstance(data, list):
        raise ValueError("Input should be a list")
    return sum(x for x in data if isinstance(x, (int, float)))


def unique_elements(data):
    if not isinstance(data, list):
        raise ValueError("Input should be a list")
    return list(set(data))

