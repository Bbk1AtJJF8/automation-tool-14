import time
import functools
import random

def retry_operation(max_attempts=3, delay=1.0, backoff=2.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            current_delay = delay
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    time.sleep(current_delay + random.uniform(0, 0.1))
                    current_delay *= backoff
        return wrapper
    return decorator

@retry_operation(max_attempts=3, delay=0.5)
def fetch_data(url):
    # Simulate volatile network state
    if random.random() < 0.7:
        raise ConnectionError("Transient network glitch")
    return {"status": "success", "data": [1, 2, 3]}

if __name__ == "__main__":
    result = fetch_data("https://api.example.com")
    print(result)