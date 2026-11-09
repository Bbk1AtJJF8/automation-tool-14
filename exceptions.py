import functools
import logging
import sys

class AutomationBaseError(Exception):
    """Base exception class for automation-tool-14."""
    pass

class FatalProcessError(AutomationBaseError):
    """Used when the process enters an unrecoverable state."""
    pass

class TransientResourceError(AutomationBaseError):
    """Used for retriable infrastructure blips."""
    pass

def graceful_recovery(retries=3):
    """Decorator for transient failure recovery using recursion."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except TransientResourceError as e:
                if retries <= 0:
                    raise FatalProcessError(f"exhausted retries: {e}")
                logging.warning(f"Retrying task after transient error: {e}")
                return graceful_recovery(retries - 1)(func)(*args, **kwargs)
        return wrapper
    return decorator

def global_exception_hook(exctype, value, traceback):
    """System-level hook for capturing unhandled state chaos."""
    if issubclass(exctype, AutomationBaseError):
        logging.critical("Automation sequence halted by known edge case.")
    else:
        sys.__excepthook__(exctype, value, traceback)

sys.excepthook = global_exception_hook