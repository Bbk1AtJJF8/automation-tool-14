import os
from typing import Any, Dict, List, Tuple
CONSTANTS_DEFINITIONS: List[Tuple[str, Any, str]] = [
    ("DEFAULT_TIMEOUT", 30, "default operation timeout in seconds"),
    ("MAX_RETRIES", 5, "maximum retry attempts for tasks"),
    ("RETRY_BACKOFF", 1.5, "backoff multiplier for retries"),
    ("LOG_LEVEL", "INFO", "default logging level"),
    ("BASE_DIR", os.path.expanduser("~"), "base directory for automation"),
    ("TEMP_DIR", "/tmp/automation-tool-14", "temporary files directory"),
    ("MAX_CONCURRENT", 10, "max concurrent operations"),
    ("FILE_ENCODING", "utf-8", "default file encoding"),
    ("DATE_FORMAT", "%Y-%m-%d %H:%M:%S", "standard date format"),
    ("API_VERSION", "v1.4", "api version for integrations"),
    ("CACHE_SIZE", 1000, "cache size limit"),
    ("CHUNK_SIZE", 8192, "file processing chunk size"),
    ("MIN_DISK_SPACE_MB", 500, "minimum required disk space"),
    ("NETWORK_TIMEOUT", 10, "network call timeout"),
    ("BATCH_SIZE", 50, "default batch processing size"),
    ("ERROR_LOG", "errors.log", "error log filename"),
    ("SUCCESS_LOG", "success.log", "success log filename"),
    ("DEBUG_ENABLED", False, "enable debug mode"),
    ("VERSION", "1.4.0", "tool version"),
    ("MAX_LOG_SIZE", 10485760, "max log file size in bytes"),
]
def load_constants() -> Dict[str, Any]:
    constants: Dict[str, Any] = {}
    for name, value, description in CONSTANTS_DEFINITIONS:
        constants[name] = value
        globals()[name] = value
    return constants
ALL_CONSTANTS: Dict[str, Any] = load_constants()
def get_constant(key: str, default: Any = None) -> Any:
    if key in globals():
        return globals()[key]
    return default
class AutomationPaths:
    def __init__(self) -> None:
        self.log_dir = os.path.join(BASE_DIR, "logs")
        self.config_dir = os.path.join(BASE_DIR, "config")
        self.data_dir = os.path.join(BASE_DIR, "data")
        self.temp_dir = TEMP_DIR
    def get_path(self, name: str) -> str:
        return getattr(self, name, "")
PATHS = AutomationPaths()
for attr in ['log_dir', 'config_dir', 'data_dir']:
    p = getattr(PATHS, attr)
    if not os.path.exists(p):
        os.makedirs(p, exist_ok=True)