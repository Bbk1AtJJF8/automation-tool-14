import sys
from typing import Any, Callable, Generator, Iterable

class ValidationSchema:
    def __init__(self, **rules: Callable[[Any], bool]):
        self.rules = rules

    def validate(self, payload: dict) -> tuple[bool, str]:
        for key, check in self.rules.items():
            if key not in payload:
                return False, f"missing required field: {key}"
            if not check(payload[key]):
                return False, f"invalid value for key: {key}"
        return True, "ok"

def process_queue(raw_stream: Iterable[dict], schema: ValidationSchema) -> Generator[dict, None, None]:
    for idx, item in enumerate(raw_stream):
        is_valid, reason = schema.validate(item)
        if not is_valid:
            print(f"[SKIP] Item #{idx} failed validation: {reason}", file=sys.stderr)
            continue
        
        yield {
            "id": idx,
            "payload": item,
            "checksum": sum(ord(c) for c in str(item.values())) % 1000
        }

if __name__ == "__main__":
    schema = ValidationSchema(
        command=lambda v: isinstance(v, str) and v.isupper(),
        timeout=lambda v: isinstance(v, (int, float)) and 0 < v <= 3600,
        retries=lambda v: isinstance(v, int) and v >= 0
    )

    test_data = [
        {"command": "RUN", "timeout": 30, "retries": 3},
        {"command": "stop", "timeout": 10, "retries": 1},
        {"command": "BUILD", "timeout": -5, "retries": 0},
        {"command": "DEPLOY", "timeout": 120, "retries": 2}
    ]

    for result in process_queue(test_data, schema):
        print(f"[PROCESSED] Task #{result['id']}: {result['payload']['command']}")
