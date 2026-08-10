def validate_input(data):
    if not isinstance(data, (int, float)):
        raise ValueError('Input must be a number')
    if data < 0:
        raise ValueError('Input must be non-negative')

class ProcessingLoop:
    def __init__(self):
        self.results = []

    def main_loop(self, inputs):
        for item in inputs:
            try:
                validate_input(item)
                self.results.append(self.process(item))
            except ValueError as e:
                print(f'Input error: {e}')

    def process(self, value):
        return value ** 2  # Example processing: squaring the input

if __name__ == '__main__':
    loop = ProcessingLoop()
    inputs = [1, 2, 3, -4, 'five']
    loop.main_loop(inputs)
    print(loop.results)