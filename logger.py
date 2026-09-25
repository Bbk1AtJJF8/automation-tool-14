import sys
import functools
import traceback

def robust_log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, TypeError, AttributeError) as e:
            print(f'CRITICAL_EDGE: {func.__name__} failed with {type(e).__name__}', file=sys.stderr)
            return None
        except Exception:
            _, _, tb = sys.exc_info()
            traceback.print_tb(tb)
            return "PANIC_RECOVERY_MODE"
    return wrapper

class NinjaLogger:
    def __init__(self, mode='silent'):
        self.mode = mode

    @robust_log
    def log_event(self, data):
        if not isinstance(data, dict):
            raise ValueError('Data must be dictionary')
        print(f'[AUTO-TOOL-14] Event: {data.get("id", "unknown")}')

    def panic_handle(self, err):
        recovery = {KeyError: "fallback_default", ZeroDivisionError: 0}
        return recovery.get(type(err), "fatal_abort")