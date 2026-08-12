import time
import random
import requests

class RetryException(Exception):
    pass

def retry_request(url, max_retries=5, delay=2, backoff=2):
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries == max_retries:
                raise RetryException(f'Failed after {max_retries} attempts') from e
            wait_time = delay * (backoff ** (retries - 1)) + random.uniform(0, 1)
            time.sleep(wait_time)
            print(f'Retrying {url}, attempt {retries}')