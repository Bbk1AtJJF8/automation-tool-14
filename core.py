import json
import os

class DataHandler:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = self.load_data() 

    def load_data(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as file:
                return json.load(file)
        return {}

    def save_data(self):
        with open(self.filepath, 'w') as file:
            json.dump(self.data, file, indent=4)

    def update_data(self, key, value):
        self.data[key] = value
        self.save_data() 

    def get_data(self, key, default=None):
        return self.data.get(key, default)

    def delete_data(self, key):
        if key in self.data:
            del self.data[key]
            self.save_data()

    def clear_data(self):
        self.data.clear()
        self.save_data()