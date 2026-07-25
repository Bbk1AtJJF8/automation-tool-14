import time
import random

def retry_operation(max_attempts, delay):
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    print(f'Operation failed: {e}. Retrying... (Attempt {attempts})')
                    time.sleep(delay)
                    # Introduce jitter to prevent thundering herd
                    jitter = random.uniform(0, delay / 2)
                    time.sleep(jitter)
            print('Max attempts reached. Operation failed.')
            return None
        return wrapper
    return decorator

@retry_operation(max_attempts=5, delay=2)
def network_call():
    if random.choice([True, False]):  # Simulate success or failure
        print('Network call succeeded.')
        return 'Success'
    else:
        raise Exception('Network error occurred')