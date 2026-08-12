import time
import random
import requests

def retry_on_failure(max_attempts=3, delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.RequestException as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    time.sleep(delay + random.uniform(0, 1))  # Exponential backoff with some randomness
        return wrapper
    return decorator

@retry_on_failure(max_attempts=5, delay=2)
def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()  # Return JSON content