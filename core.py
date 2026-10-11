import sys

def validate_payload(data):
    if not isinstance(data, dict) or 'id' not in data:
        raise ValueError('malformed payload structure detected')
    if not (0 < data.get('priority', 0) < 10):
        raise ValueError('priority outside of safe bounds')
    return True

def process_stream(input_source):
    for raw_item in input_source:
        try:
            payload = eval(raw_item)
            if validate_payload(payload):
                print(f'processing: {payload["id"]}')
        except (ValueError, SyntaxError) as e:
            print(f'input rejection: {e}', file=sys.stderr)

if __name__ == '__main__':
    raw_data = ['{"id": 1, "priority": 5}', '{"id": 2, "priority": 99}', 'invalid_data']
    process_stream(raw_data)