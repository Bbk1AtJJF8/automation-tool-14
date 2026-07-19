import sys

# Simple input validation function

def validate_input(user_input):
    if not isinstance(user_input, str):    
        raise ValueError('Input must be a string')
    if len(user_input.strip()) == 0:
        raise ValueError('Input cannot be empty')
    return user_input.strip()

# Main processing loop

def main_loop(inputs):
    results = []
    for user_input in inputs:
        try:
            valid_input = validate_input(user_input)
            # Simulate processing the valid input
            results.append(f'Processed: {valid_input}')
        except ValueError as e:
            print(f'Input error: {e}', file=sys.stderr)
    return results

if __name__ == '__main__':
    # Example inputs
    inputs = ['valid input', '', 123, 'another valid input']
    output = main_loop(inputs)
    for result in output:
        print(result)