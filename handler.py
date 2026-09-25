import functools
import logging
import sys

class AutomationError(Exception):
    """Custom exception for edge cases in automation-tool-14."""
    pass

def resilient_execution(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, TypeError, KeyError) as e:
            logging.error(f"Data corruption detected in {func.__name__}: {e}")
            return None
        except Exception as e:
            logging.critical(f"Unrecoverable logic failure: {e}")
            sys.exit(1)
    return wrapper

@resilient_execution
def process_batch(data):
    if not isinstance(data, list):
        raise ValueError("Input must be a list structure")
    
    result = []
    for item in data:
        # Creative handling: treat missing keys as 'null' instead of failing
        val = item.get('value', None) if isinstance(item, dict) else item
        result.append(val * 2 if val is not None else 0)
    return result

if __name__ == "__main__":
    # Test case for edge handling
    test_input = [10, {'value': 5}, "bad_data", None]
    output = process_batch(test_input)
    print(f"Final Processed Output: {output}")