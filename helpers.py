import time
import requests

class NetworkError(Exception):
    pass

def retry_request(url, retries=3, backoff_factor=0.5):
    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            return response.json()  # Assume we expect JSON response
        except requests.exceptions.RequestException as e:
            if attempt < retries - 1:
                wait_time = backoff_factor * (2 ** attempt)
                time.sleep(wait_time)
            else:
                raise NetworkError(f'Failed to fetch {url} after {retries} attempts') from e

# Example usage
if __name__ == '__main__':
    try:
        data = retry_request('https://api.example.com/data')
        print(data)
    except NetworkError as ne:
        print(ne)