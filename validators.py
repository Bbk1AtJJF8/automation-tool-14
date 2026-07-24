import re

class ValidationError(Exception):
    pass


def validate_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        raise ValidationError(f'Invalid email: {email}')  
    return True


def validate_phone(phone):
    phone_regex = r'^(\+\d{1,3})?\d{10}$'
    if not re.match(phone_regex, phone):
        raise ValidationError(f'Invalid phone number: {phone}')  
    return True


def validate_age(age):
    if not isinstance(age, int):
        raise ValidationError(f'Age must be an integer, got {type(age).__name__}')  
    if age < 0 or age > 120:
        raise ValidationError(f'Age must be between 0 and 120, got {age}')  
    return True


if __name__ == '__main__':
    try:
        validate_email('test@example.com')
        validate_phone('+1234567890')
        validate_age(30)
    except ValidationError as e:
        print(e)