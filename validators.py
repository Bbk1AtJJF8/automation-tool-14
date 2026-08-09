import re

class ValidationError(Exception):
    pass

class InputValidator:
    def validate_email(self, email):
        if not isinstance(email, str):
            raise ValidationError("Email must be a string")
        if not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email):
            raise ValidationError("Invalid email format")
        return True

    def validate_age(self, age):
        if not isinstance(age, int):
            raise ValidationError("Age must be an integer")
        if age < 0:
            raise ValidationError("Age cannot be negative")
        return True

    def validate_username(self, username):
        if not isinstance(username, str):
            raise ValidationError("Username must be a string")
        if len(username) < 3 or len(username) > 20:
            raise ValidationError("Username must be between 3 and 20 characters")
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationError("Username can only contain letters, numbers, and underscores")
        return True