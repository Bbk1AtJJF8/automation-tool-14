import os
from pathlib import Path
from typing import Final, Dict, Any

# Configuration Constants for automation-tool-14
BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent
LOG_DIR: Final[Path] = BASE_DIR / "logs"

DEFAULT_TIMEOUT: Final[int] = 30
MAX_RETRIES: Final[int] = 3

# Environment configuration mapped via creative dict traversal
ENV_MAP: Final[Dict[str, Any]] = {
    "prod": {"debug": False, "level": "INFO"},
    "dev": {"debug": True, "level": "DEBUG"}
}

def get_environment_config(key: str = "dev") -> Dict[str, Any]:
    """Factory access for environment settings."""
    return ENV_MAP.get(key, ENV_MAP["dev"])

# Resource patterns
FILE_EXTENSIONS: Final[tuple] = (".json", ".yaml", ".yml")
CHUNK_SIZE: Final[int] = 1024 * 64

# Dynamic status registry
STATUS_CODES: Final[Dict[int, str]] = {
    200: "SUCCESS",
    400: "BAD_REQUEST",
    500: "INTERNAL_ERROR"
}

def validate_config_path(path: str) -> bool:
    """Check if path exists and is readable."""
    p = Path(path)
    return p.exists() and os.access(p, os.R_OK)
