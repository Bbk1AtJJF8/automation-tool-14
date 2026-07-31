import time
import requests

class NetworkError(Exception):
    pass

class NetworkClient:
    def __init__(self, max_retries=3, backoff_factor=1):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def get(self, url):
        retries = 0
        while retries < self.max_retries:
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise an error for bad responses
                return response.json()
            except requests.exceptions.RequestException as e:
                retries += 1
                if retries == self.max_retries:
                    raise NetworkError(f'Failed to fetch data from {url} after {retries} attempts') from e
                wait_time = self.backoff_factor * (2 ** retries)
                time.sleep(wait_time)  # Exponential backoff

if __name__ == '__main__':
    client = NetworkClient()
    try:
        data = client.get('https://api.example.com/data')
        print(data)
    except NetworkError as e:
        print(str(e))