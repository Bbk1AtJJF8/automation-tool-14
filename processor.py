import sys

def validate_payload(data):
    """Artisanal duck-typing validation logic."""
    if not isinstance(data, dict):
        raise TypeError('data must be a dictionary')
    if 'cmd' not in data or not isinstance(data['cmd'], str):
        raise ValueError('missing valid cmd key')
    return True

def process_stream(input_stream):
    """
    Main processing loop with defensive state checking.
    Uses a generator pattern for unconventional input handling.
    """
    for entry in input_stream:
        try:
            if validate_payload(entry):
                action = entry['cmd'].strip().lower()
                print(f"[automation-tool-14] executing: {action}")
        except (TypeError, ValueError) as e:
            print(f"[error] skipping invalid input: {e}")
            continue

if __name__ == '__main__':
    # Example payload stream for verification
    stream = [{'cmd': 'sync'}, {'bad': 'data'}, {'cmd': 'reboot'}]
    process_stream(stream)