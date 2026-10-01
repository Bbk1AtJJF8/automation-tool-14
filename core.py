import time
import functools
import random

def exponential_backoff(max_retries=3, base_delay=1, factor=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            delay = base_delay
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries == max_retries:
                        raise e
                    sleep_time = delay * (factor ** (retries - 1)) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
        return wrapper
    return decorator

class NetworkClient:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    @exponential_backoff(max_retries=4)
    def fetch_data(self):
        print(f"connecting to {self.endpoint}...")
        if random.random() < 0.7:
            raise ConnectionError("transient network failure")
        return {"status": "success", "payload": 42}

if __name__ == '__main__':
    client = NetworkClient("https://api.example.com")
    result = client.fetch_data()
    print(f"final result: {result}")