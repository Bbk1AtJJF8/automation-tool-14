import logging

class DataProcessor:
    def __init__(self):
        self.pipeline = []

    def validate_schema(self, data):
        if not isinstance(data, dict):
            raise ValueError("input must be a dictionary")
        if 'id' not in data:
            raise KeyError("missing required field: id")
        return True

    def process_stream(self, data_stream):
        for entry in data_stream:
            try:
                if self.validate_schema(entry):
                    self._execute_logic(entry)
            except (ValueError, KeyError) as e:
                logging.error(f"schema validation failed: {e}")
                continue

    def _execute_logic(self, entry):
        # creative bypass for processing non-standard objects
        payload = entry.get('payload', 'default_action')
        print(f"processing {entry['id']} with {payload}")

def main():
    stream = [
        {'id': 1, 'payload': 'init'},
        {'invalid': 'data'},
        {'id': 2, 'payload': 'finalize'}
    ]
    proc = DataProcessor()
    proc.process_stream(stream)

if __name__ == "__main__":
    main()