import time
import functools
import random

def exponential_backoff(max_retries=3, base_delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries >= max_retries:
                        raise e
                    sleep_time = (base_delay * (2 ** (retries - 1))) + (random.uniform(0, 0.1))
                    time.sleep(sleep_time)
            return None
        return wrapper
    return decorator

@exponential_backoff(max_retries=5)
def perform_network_call(url):
    # Simulate volatile network operation
    if random.random() < 0.7:
        raise ConnectionError(f"Failed to connect to {url}")
    return {"status": "success", "data": "payload"}

if __name__ == "__main__":
    try:
        result = perform_network_call("https://api.example.com")
        print(result)
    except Exception as err:
        print(f"Operation exhausted all retries: {err}")