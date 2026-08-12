MAX_CONNECTIONS = 100
MAX_RETRIES = 5
TIMEOUT_SECONDS = 30
API_BASE_URL = 'https://api.example.com/'
DEFAULT_HEADERS = {'Content-Type': 'application/json'}
SUCCESS_STATUS_CODES = {200, 201, 202}
ERROR_STATUS_CODES = {400, 404, 500}

class LogLevel:
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

SUPPORTED_FORMATS = ['json', 'xml', 'csv']
DAYS_IN_WEEK = 7
DEFAULT_CURRENCY = 'USD'

def convert_currency(amount, rate):
    return amount * rate

def get_api_endpoint(endpoint):
    return f'{API_BASE_URL}{endpoint}'

# Constants for pagination
PAGE_SIZE = 20
MAX_PAGE_LIMIT = 100

exported_constants = {
    'MAX_CONNECTIONS': MAX_CONNECTIONS,
    'MAX_RETRIES': MAX_RETRIES,
    'TIMEOUT_SECONDS': TIMEOUT_SECONDS
}

if __name__ == '__main__':
    print('Constants module loaded successfully.')