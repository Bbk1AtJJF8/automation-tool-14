import re

class Validator:
    def __init__(self):
        self.email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        self.phone_pattern = re.compile(r'^\+?1?\d{10,15}$')

    def is_valid_email(self, email: str) -> bool:
        return bool(self.email_pattern.match(email))

    def is_valid_phone(self, phone: str) -> bool:
        return bool(self.phone_pattern.match(phone))

    def validate(self, email: str, phone: str) -> dict:
        return {
            'email': self.is_valid_email(email),
            'phone': self.is_valid_phone(phone)
        }

if __name__ == '__main__':
    validator = Validator()  
    test_email = 'test@example.com'
    test_phone = '+1234567890'
    print(validator.validate(test_email, test_phone))
    # Example outputs the validity of the test inputs