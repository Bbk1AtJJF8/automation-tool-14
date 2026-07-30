import re

class Validator:
    def __init__(self):
        self.patterns = {
            'email': re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$'),
            'url': re.compile(r'^(http|https)://[\w.-]+(\.[\w.-]+)+[/\w .-]*?$'),
            'phone': re.compile(r'^(\+?\d{1,3}[- ]?)?\(?\d{1,4}\)?[- ]?\d{1,4}[- ]?\d{1,9}$')
        }

    def validate(self, value, type_):
        if type_ not in self.patterns:
            raise ValueError(f'Unknown validation type: {type_}')
        return bool(self.patterns[type_].match(value))

    def validate_multiple(self, values, type_):
        return {value: self.validate(value, type_) for value in values}

# Usage example:
if __name__ == '__main__':
    validator = Validator()
    emails = ['test@example.com', 'invalid-email']
    results = validator.validate_multiple(emails, 'email')
    print(results)  # Output: {'test@example.com': True, 'invalid-email': False}