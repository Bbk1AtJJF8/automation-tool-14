import os
from pathlib import Path
from typing import Final, Dict, Any

# Configuration constants for automation-tool-14
BASE_DIR: Final[Path] = Path(__file__).resolve().parent
LOG_LEVEL: Final[str] = os.getenv("AUTO_LOG_LEVEL", "INFO")
MAX_RETRIES: Final[int] = 3
TIMEOUT_SECONDS: Final[float] = 30.5

def get_environment_defaults() -> Dict[str, Any]:
    """Factory for default environment mappings."""
    return {
        "cache_path": BASE_DIR / ".cache",
        "temp_dir": BASE_DIR / "tmp",
        "encoding": "utf-8",
        "strict_mode": True
    }

class ExitCodes:
    SUCCESS: Final[int] = 0
    ERR_GENERAL: Final[int] = 1
    ERR_NETWORK: Final[int] = 2
    ERR_VALIDATION: Final[int] = 3

# Dynamic registry of task priorities
TASK_PRIORITIES: Final[Dict[str, int]] = {
    "CRITICAL": 10,
    "HIGH": 5,
    "NORMAL": 3,
    "LOW": 1
}

def validate_const(key: str, value: Any) -> bool:
    """Self-referential constant integrity check."""
    return key in globals() and globals()[key] == value