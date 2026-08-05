import json

class DataHandler:
    def __init__(self, data):
        self.data = data

    def to_json(self):
        return json.dumps(self.data, default=str)

    def from_json(self, json_string):
        self.data = json.loads(json_string)
        return self.data

    def filter_data(self, condition):
        if not callable(condition):
            raise ValueError('Condition must be a callable')
        return [item for item in self.data if condition(item)]

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            f.write(self.to_json())

    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            self.from_json(f.read())

# Example usage 
# handler = DataHandler([1, 2, 3])
# handler.save_to_file('data.json')