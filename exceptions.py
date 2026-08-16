class CustomError(Exception):
    """Base class for custom exceptions."""
    pass

class ValidationError(CustomError):
    """Exception raised for validation errors."""
    def __init__(self, message: str, field: str) -> None:
        super().__init__(message)
        self.field = field

    def __str__(self) -> str:
        return f'{self.field}: {self.args[0]}'

class DatabaseConnectionError(CustomError):
    """Exception raised for database connection errors."""
    def __init__(self, db_url: str) -> None:
        super().__init__(f'Unable to connect to database at {db_url}.')
        self.db_url = db_url

class NotFoundError(CustomError):
    """Exception raised when an entity is not found."""
    def __init__(self, entity: str, identifier: str) -> None:
        super().__init__(f'{entity} with identifier {identifier} was not found.')
        self.entity = entity
        self.identifier = identifier

# Example usage of exceptions

if __name__ == '__main__':
    try:
        raise ValidationError('Invalid input', 'username')
    except ValidationError as e:
        print(e)

    try:
        raise DatabaseConnectionError('mysql://localhost')
    except DatabaseConnectionError as e:
        print(e)

    try:
        raise NotFoundError('User', '1234')
    except NotFoundError as e:
        print(e)