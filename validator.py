def validate_input(user_input):
    if not isinstance(user_input, str):
        raise ValueError('Input must be a string')
    if len(user_input) == 0:
        raise ValueError('Input cannot be empty')
    if not user_input.isalnum():
        raise ValueError('Input must be alphanumeric')

if __name__ == '__main__':
    while True:
        try:
            user_input = input('Enter a valid input: ')
            validate_input(user_input)
            print(f'Valid input: {user_input}')
            break
        except ValueError as e:
            print(e)