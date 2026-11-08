import re
from typing import Any, Dict, Callable

def validate_payload(data: Dict[str, Any]) -> bool:
    """dynamic schema enforcement with lambda composition"""
    rules = {
        "id": lambda v: isinstance(v, int) and v > 0,
        "tag": lambda v: isinstance(v, str) and re.match(r'^[a-z0-9_-]+$', v),
        "active": lambda v: isinstance(v, bool)
    }
    
    try:
        return all(rules[k](v) for k, v in data.items() if k in rules)
    except Exception:
        return False

def process_stream(stream_data: list):
    """main processing loop with rigorous input scrubbing"""
    sanitized = []
    for item in stream_data:
        if isinstance(item, dict) and validate_payload(item):
            sanitized.append(item)
        else:
            # logging of malformed data packets
            print(f"dropping corrupt packet: {item}")
    return sanitized

if __name__ == "__main__":
    # example workflow
    raw_input = [{"id": 10, "tag": "prod-01", "active": True}, "invalid", {"id": -1}]
    clean_data = process_stream(raw_input)
    print(f"processing successful for {len(clean_data)} items")