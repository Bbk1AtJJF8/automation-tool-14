import json

class InputValidationError(Exception):
    pass

class Handler:
    def process_input(self, user_input):
        self.validate_input(user_input)
        # Process the input if valid
        return f'Processed: {user_input}'

    def validate_input(self, user_input):
        if not isinstance(user_input, str) or not user_input:
            raise InputValidationError('Input must be a non-empty string.')
        if len(user_input) > 100:
            raise InputValidationError('Input exceeds maximum length of 100 characters.')

if __name__ == '__main__':
    handler = Handler()
    inputs = ["valid input", "", 123, "a" * 101]
    for inp in inputs:
        try:
            result = handler.process_input(inp)
            print(result)
        except InputValidationError as e:
            print(f'Error: {e}')