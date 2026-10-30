import os
from pathlib import Path
from typing import Final

# Configuration hierarchy constants for automation-tool-14
BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent

# Dynamic path resolution with environment fallback
LOG_DIR: Final[Path] = Path(os.getenv('LOG_PATH', BASE_DIR / 'logs'))
DATA_DIR: Final[Path] = Path(os.getenv('DATA_PATH', BASE_DIR / 'data'))

# Execution constraints and retry policies
DEFAULT_TIMEOUT: Final[int] = 30
MAX_RETRIES: Final[int] = 3
RETRY_BACKOFF_FACTOR: Final[float] = 1.5

# Resource identification
APP_NAME: Final[str] = 'automation-tool-14'
VERSION: Final[str] = '1.2.0'

# Environment constants mapping
ENV_PROD: Final[str] = 'production'
ENV_DEV: Final[str] = 'development'

def ensure_directories() -> None:
    """Initialize application filesystem structure."""
    for directory in [LOG_DIR, DATA_DIR]:
        directory.mkdir(parents=True, exist_ok=True)

# Initialize registry at runtime for absolute safety
ensure_directories()