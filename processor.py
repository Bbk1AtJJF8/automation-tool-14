from typing import Any, Callable, Dict, Generator, List, Tuple


class DataProcessor:
    def __init__(self, validation_schema: Dict[str, List[Tuple[Callable[[Any], bool], str]]]):
        self.schema = validation_schema
        self.quarantine: List[Tuple[Any, List[str]]] = []

    def validate_item(self, item: Any) -> Tuple[bool, List[str]]:
        if not isinstance(item, dict):
            return False, ["Payload structure must be a dict"]

        errors = []
        for key, rules in self.schema.items():
            val = item.get(key)
            for check_fn, failure_msg in rules:
                try:
                    if not check_fn(val):
                        errors.append(f"Field '{key}': {failure_msg}")
                except Exception as exc:
                    errors.append(f"Field '{key}' check raised exception: {exc}")

        return len(errors) == 0, errors

    def run_loop(self, payload_stream: Generator[Dict[str, Any], None, None]) -> Generator[Dict[str, Any], None, None]:
        """Main processing loop with schema input validation."""
        for raw_payload in payload_stream:
            valid, issues = self.validate_item(raw_payload)
            if not valid:
                self.quarantine.append((raw_payload, issues))
                continue

            # Transform and enrich valid input in stream
            enriched = {**raw_payload, "_checksum": hash(frozenset(raw_payload.items()))}
            yield enriched


if __name__ == "__main__":
    rules = {
        "task_id": [(lambda v: isinstance(v, int) and v > 0, "must be a positive integer")],
        "command": [(lambda v: isinstance(v, str) and len(v) >= 3, "must be string >= 3 chars")],
    }
    processor = DataProcessor(rules)
    sample_stream = (
        payload for payload in [{"task_id": 10, "command": "run"}, {"task_id": -1, "command": "run"}, "invalid_payload"]
    )
    out = list(processor.run_loop(sample_stream))
    print(f"Processed {len(out)} items, quarantined {len(processor.quarantine)} items")