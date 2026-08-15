class CustomError(Exception):
    """Custom exception for specific errors during processing."""
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

class ValidationError(CustomError):
    """Exception raised for validation errors."""
    def __init__(self, field: str, message: str) -> None:
        super().__init__(message)
        self.field = field

class ConnectionError(CustomError):
    """Exception raised for connection-related issues."""
    def __init__(self, code: int, message: str) -> None:
        super().__init__(message)
        self.code = code

def handle_error(err: CustomError) -> None:
    """Handles exceptions by logging the error message."""
    print(f'Error: {err.message}')
    if isinstance(err, ValidationError):
        print(f'Validation failed for field: {err.field}')
    elif isinstance(err, ConnectionError):
        print(f'Connection error code: {err.code}')