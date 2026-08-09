import re

def validate_email(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$'
    return re.match(regex, email) is not None

def validate_phone(phone):
    regex = r'^\+?1?\d{9,15}$'
    return re.match(regex, phone) is not None

class Validator:
    def __init__(self):
        self.validation_methods = {
            'email': validate_email,
            'phone': validate_phone,
        }

    def validate(self, value_type, value):
        if value_type in self.validation_methods:
            return self.validation_methods[value_type](value)
        raise ValueError(f'Unknown validation type: {value_type}')