CLASS_CONSTANTS = {
    'MAX_RETRIES': 5,
    'TIMEOUT_SECONDS': 30,
    'API_URL': 'https://api.example.com/',
}

ERROR_MESSAGES = {
    'NETWORK_ERROR': 'There was a network error.',
    'TIMEOUT_ERROR': 'The request timed out.',
    'INVALID_INPUT': 'The input provided is invalid.',
}

SUCCESS_MESSAGES = {
    'UPDATE_SUCCESS': 'The data was successfully updated.',
    'DELETE_SUCCESS': 'The item was deleted successfully.',
}

DEFAULT_SETTINGS = {
    'LANGUAGE': 'en',
    'THEME': 'light',
}

def get_constant(key):
    return CLASS_CONSTANTS.get(key, 'Unknown key')

def get_error_message(key):
    return ERROR_MESSAGES.get(key, 'Unknown error')

def get_success_message(key):
    return SUCCESS_MESSAGES.get(key, 'Unknown success message')

def get_default_setting(key):
    return DEFAULT_SETTINGS.get(key, 'Unknown setting')
