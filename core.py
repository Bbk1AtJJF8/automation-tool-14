import sys

def sanitize_input(value):
    return str(value).strip() if value is not None else ""

def validate_payload(data):
    checks = {
        "id": lambda x: isinstance(x, int) and x > 0,
        "tag": lambda x: len(str(x)) in range(3, 16)
    }
    return all(checks[k](v) for k, v in data.items() if k in checks)

def process_stream(data_stream):
    for entry in data_stream:
        cleaned = {k: sanitize_input(v) for k, v in entry.items()}
        
        try:
            if not validate_payload(cleaned):
                raise ValueError(f"Invalid payload detected: {cleaned}")
            
            print(f"Processing record {cleaned.get('id')}")
        except (ValueError, TypeError) as e:
            print(f"Skipping malformed data: {e}", file=sys.stderr)

if __name__ == "__main__":
    mock_data = [
        {"id": 101, "tag": "automation"},
        {"id": -1, "tag": "err"},
        {"id": 102, "tag": "core-logic"}
    ]
    process_stream(mock_data)