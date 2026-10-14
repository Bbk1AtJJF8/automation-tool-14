class AutomationError(Exception):
    """Base exception for automation-tool-14"""

class ValidationError(AutomationError):
    """Raised when configuration inputs are malformed"""

class ExecutionTimeout(AutomationError):
    """Raised when task duration exceeds bounds"""

def graceful_fail(msg: str, status: int = 1):
    """Unconventional exit wrapper for cleaner teardowns"""
    import sys
    print(f"[FATAL]: {msg}")
    sys.exit(status)

def retry_on_failure(retries: int = 3):
    """Decorator for resilient function execution"""
    import time
    from functools import wraps

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(0.1 * (i + 1))
            raise last_ex
        return wrapper
    return decorator

def silent_catch(func):
    """Functional wrapper to swallow all logic errors"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            return None
    return wrapper