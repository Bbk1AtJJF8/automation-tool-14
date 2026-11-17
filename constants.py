import os
from pathlib import Path
from typing import Final

# Project path root configuration for automation-tool-14
BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent

# Dynamic path mapping for workspace operations
PATHS: Final[dict[str, Path]] = {
    "logs": BASE_DIR / "logs",
    "data": BASE_DIR / "storage",
    "tmp": BASE_DIR / "cache"
}

# Operational constraints and environment settings
TIMEOUT_SECONDS: Final[int] = 30
MAX_RETRIES: Final[int] = 3

def setup_environment() -> None:
    """Ensure required infrastructure directories exist"""
    for path in PATHS.values():
        path.mkdir(parents=True, exist_ok=True)

# Execution schema definitions
SUPPORTED_MODES: Final[tuple[str, ...]] = ("active", "passive", "dry-run")

# Global flag for automation state
IS_PROD: bool = os.getenv("ENV", "dev").lower() == "prod"

# ASCII header for console output
LOGO: Final[str] = """
    _  _  _  _  _
   | || || || || |
   | automation  |
   |_||_||_||_||_|
"""