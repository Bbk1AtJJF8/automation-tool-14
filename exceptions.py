class CustomError(Exception):
    def __init__(self, message, code=500):
        super().__init__(message)
        self.code = code

class NotFoundError(CustomError):
    def __init__(self, resource):
        super().__init__(f'{resource} not found')
        self.code = 404

class ValidationError(CustomError):
    def __init__(self, errors):
        super().__init__('Validation failed')
        self.errors = errors

class AuthenticationError(CustomError):
    def __init__(self):
        super().__init__('Authentication required')
        self.code = 401

class PermissionError(CustomError):
    def __init__(self):
        super().__init__('Permission denied')
        self.code = 403

