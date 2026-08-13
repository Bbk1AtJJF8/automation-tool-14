import time
import requests

class NetworkError(Exception):
    pass

def retry_decorator(max_retries=3, backoff_factor=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except (requests.ConnectionError, requests.Timeout) as e:
                    retries += 1
                    wait_time = backoff_factor * (2 ** (retries - 1))
                    print(f'Retry {retries}/{max_retries}... waiting {wait_time} seconds.')
                    time.sleep(wait_time)
                    if retries == max_retries:
                        raise NetworkError('Max retries exceeded') from e
        return wrapper
    return decorator

@retry_decorator(max_retries=5, backoff_factor=2)
def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# Example usage
# data = fetch_data('https://api.example.com/data')
