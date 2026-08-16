import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Handler:
    def __init__(self, data):
        self.data = data

    def process_data(self):
        try:
            processed = self._clean_data(self.data)
            return json.dumps(processed)
        except Exception as e:
            logger.error(f"Error processing data: {e}")
            return None

    def _clean_data(self, data):
        cleaned_data = {k: v for k, v in data.items() if v is not None}
        logger.info("Data cleaned successfully")
        return cleaned_data

if __name__ == '__main__':
    sample_data = {"name": "John", "age": None, "city": "New York"}
    handler = Handler(sample_data)
    result = handler.process_data()
    print(result)  # Should print cleaned JSON data