import json
import logging

class CustomError(Exception):
    pass

class ErrorHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.ERROR)

    def handle_error(self, error):
        if isinstance(error, CustomError):
            self.logger.error(f'CustomError occurred: {error}')
            return {'status': 'error', 'message': str(error)}
        elif isinstance(error, ValueError):
            self.logger.error('ValueError: Invalid value provided')
            return {'status': 'error', 'message': 'Invalid value'}
        elif isinstance(error, KeyError):
            self.logger.error('KeyError: Key not found')
            return {'status': 'error', 'message': 'Key not found'}
        else:
            self.logger.error(f'Unknown error: {error}')
            return {'status': 'error', 'message': 'An unknown error occurred'}

    def process_request(self, request):
        try:
            # Simulate processing logic  
            if request.get('action') is None:
                raise CustomError('Action cannot be None')
            # Further processing code goes here
            return {'status': 'success', 'data': 'Processed successfully'}
        except Exception as e:
            return self.handle_error(e)

if __name__ == '__main__':
    handler = ErrorHandler()
    response = handler.process_request({'action': None})
    print(json.dumps(response))
