import json

class DataProcessor:
    def __init__(self, data):
        self.data = data

    def process(self):
        cleaned_data = self.cleanup(self.data)
        return self.transform(cleaned_data)

    def cleanup(self, data):
        return [item for item in data if item is not None]

    def transform(self, cleaned_data):
        return [json.dumps(item) for item in cleaned_data]

if __name__ == '__main__':
    sample_data = [1, 2, None, 3, None, 4]
    processor = DataProcessor(sample_data)
    result = processor.process()
    print(result)