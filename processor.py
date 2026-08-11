import time
import requests

class NetworkOperation:
    def __init__(self, retries=3, backoff=1):
        self.retries = retries
        self.backoff = backoff

    def retry_request(self, url, method='GET', **kwargs):
        attempt = 0
        while attempt < self.retries:
            try:
                if method == 'GET':
                    response = requests.get(url, **kwargs)
                elif method == 'POST':
                    response = requests.post(url, **kwargs)
                else:
                    raise ValueError('Unsupported HTTP method')
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                attempt += 1
                if attempt < self.retries:
                    time.sleep(self.backoff * (2 ** (attempt - 1)))
                    print(f'Retrying {attempt}/{self.retries}...')
                else:
                    print('Max retries exceeded')
                    raise e

if __name__ == '__main__':
    net_op = NetworkOperation(retries=5, backoff=2)
    try:
        response = net_op.retry_request('https://api.example.com/data')
        print(response.json())
    except Exception as e:
        print(f'Failed after retries: {e}')