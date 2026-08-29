import time
import json
from datetime import datetime
from typing import Any, Callable, List

MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30
BATCH_SIZE = 50
LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR"]
OPERATION_MODES = ["sequential", "parallel", "batch"]

def get_constant(key: str) -> Any:
    constants = {"max_retries": MAX_RETRIES, "timeout": DEFAULT_TIMEOUT, "batch_size": BATCH_SIZE, "log_levels": LOG_LEVELS, "modes": OPERATION_MODES}
    return constants.get(key)

def retry_with_backoff(func: Callable, *args: Any, **kwargs: Any) -> Any:
    retries = get_constant("max_retries")
    for i in range(retries):
        try:
            return func(*args, **kwargs)
        except Exception:
            if i == retries - 1:
                raise
            time.sleep(0.1 * (2 ** i))
    return None

def batch_execute(items: List[Any], action: Callable[[Any], Any]) -> List[Any]:
    size = get_constant("batch_size")
    results = []
    for start in range(0, len(items), size):
        end = start + size
        batch = items[start:end]
        results += [action(item) for item in batch]
    return results

def log_message(level: str, msg: str) -> None:
    if level in get_constant("log_levels"):
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"{ts} [{level}] {msg}")

def is_valid_mode(mode: str) -> bool:
    return mode in get_constant("modes")

def generate_handler(op_type: str) -> Callable:
    def inner(val: Any) -> Any:
        if op_type == "process":
            return val * 2 if isinstance(val, (int, float)) else str(val)
        elif op_type == "validate":
            return bool(val)
        return val
    return inner

def export_constants(path: str) -> None:
    data = {"MAX_RETRIES": MAX_RETRIES, "DEFAULT_TIMEOUT": DEFAULT_TIMEOUT, "BATCH_SIZE": BATCH_SIZE, "LOG_LEVELS": LOG_LEVELS, "OPERATION_MODES": OPERATION_MODES}
    with open(path, "w") as file:
        json.dump(data, file, indent=2)

def safe_get_constant(key: str, default: Any = None) -> Any:
    val = get_constant(key)
    return val if val is not None else default