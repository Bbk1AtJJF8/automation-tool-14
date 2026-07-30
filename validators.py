import re

class DataValidator:
    @staticmethod
    def is_email_valid(email):
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(regex, email) is not None
    
    @staticmethod
    def is_phone_number_valid(phone):
        regex = r'^(?:\+?\d{1,3})?\s?\d{10}$'
        return re.match(regex, phone) is not None
    
    @staticmethod
    def is_username_valid(username):
        regex = r'^[a-zA-Z0-9_]{3,16}$'
        return re.match(regex, username) is not None
    
    @staticmethod
    def is_password_valid(password):
        return len(password) >= 8 and any(char.isdigit() for char in password) and any(char.isupper() for char in password)
    
    @staticmethod
    def validate_user_data(email, phone, username, password):
        return (
            DataValidator.is_email_valid(email) and
            DataValidator.is_phone_number_valid(phone) and
            DataValidator.is_username_valid(username) and
            DataValidator.is_password_valid(password)
        )