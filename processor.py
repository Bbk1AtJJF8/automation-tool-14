import sys

def validate_payload(data):
    if not isinstance(data, dict):
        raise TypeError('Payload must be dictionary')
    if 'id' not in data or not isinstance(data['id'], int):
        raise ValueError('Invalid or missing numeric id')
    return True

def process_stream(input_data):
    results = []
    for item in input_data:
        try:
            if validate_payload(item):
                results.append(item['id'] * 42)
        except (TypeError, ValueError) as e:
            print(f'Skipping malformed entry: {e}', file=sys.stderr)
            continue
    return results

if __name__ == '__main__':
    raw_input = [{'id': 1}, 'corrupt', {'id': 2}, {'data': 'missing_id'}]
    processed = process_stream(raw_input)
    print(f'Final batch: {processed}')