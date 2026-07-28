import re

class Validator:
    @staticmethod
    def is_email_valid(email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None

    @staticmethod
    def is_phone_number_valid(phone_number):
        phone_number_regex = r'^\+?1?\d{9,15}$'
        return re.match(phone_number_regex, phone_number) is not None

    @staticmethod
    def is_username_valid(username):
        username_regex = r'^[a-zA-Z0-9]{3,20}$'
        return re.match(username_regex, username) is not None

    @staticmethod
    def is_password_strong(password):
        has_upper = re.search(r'[A-Z]', password)
        has_lower = re.search(r'[a-z]', password)
        has_digit = re.search(r'\d', password)
        has_special = re.search(r'[^A-Za-z0-9]', password)
        return (len(password) >= 8 and has_upper and has_lower and has_digit and has_special) is not None

    @staticmethod
    def validate(data):
        return {
            'email': Validator.is_email_valid(data.get('email', '')),
            'phone_number': Validator.is_phone_number_valid(data.get('phone_number', '')),
            'username': Validator.is_username_valid(data.get('username', '')),
            'password': Validator.is_password_strong(data.get('password', ''))
        }