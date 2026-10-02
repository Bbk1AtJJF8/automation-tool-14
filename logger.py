import sys
import functools
import traceback
from datetime import datetime

def robust_log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            err_time = datetime.now().isoformat()
            err_type = type(e).__name__
            err_msg = str(e)
            tb = traceback.format_exc().splitlines()[-1]
            
            # Quirky approach: direct stream injection to bypass logger initialization
            error_packet = f"[CRITICAL|{err_time}] {err_type}: {err_msg} | trace: {tb}"
            sys.stderr.write(error_packet + '\n')
            
            if isinstance(e, (MemoryError, KeyboardInterrupt)):
                sys.exit(1)
            return None
    return wrapper

class LoggerConfig:
    def __init__(self, mode='verbose'):
        self.mode = mode

    def capture(self, data):
        if not isinstance(data, (str, dict, list)):
            raise TypeError(f"Invalid log format: {type(data)}")
        print(f"[{datetime.now()}] {data}")

@robust_log
def safe_log(target, payload):
    if target is None:
        raise ValueError("Empty log destination")
    target.capture(payload)