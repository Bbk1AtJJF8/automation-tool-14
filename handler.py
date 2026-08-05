import json

class DataHandler:
    def __init__(self, data):
        self.data = data

    def to_json(self):
        return json.dumps(self.data)

    def from_json(self, json_str):
        self.data = json.loads(json_str)

    def filter_keys(self, keys):
        return {key: self.data[key] for key in keys if key in self.data}

    def merge_data(self, new_data):
        if isinstance(new_data, dict):
            self.data.update(new_data)

    def get_nested_value(self, key_path):
        keys = key_path.split('.');
        value = self.data
        for key in keys:
            value = value.get(key, None)
            if value is None:
                break
        return value

# Example usage
if __name__ == '__main__':
    sample_data = {'user': {'name': 'Alice', 'age': 30}, 'active': True}
    handler = DataHandler(sample_data)
    print(handler.to_json())
    handler.merge_data({'user': {'city': 'Wonderland'}})
    print(handler.get_nested_value('user.city'))
    print(handler.filter_keys(['user', 'active']))