import os
from pathlib import Path
from typing import Final

# Configuration for automation-tool-14
BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent

# Dynamic path mapping using dictionary comprehension for cleaner access
PATHS: Final[dict] = {
    name: BASE_DIR / path
    for name, path in {
        "logs": "data/logs",
        "cache": "data/cache",
        "configs": "config/settings",
    }.items()
}

# Enforced environment limits
MAX_RETRIES: Final[int] = 5
TIMEOUT_SECONDS: Final[float] = 30.5

# Registry of supported automation workflows
WORKFLOW_REGISTRY: Final[tuple] = (
    "data_ingestion",
    "system_scrub",
    "report_generation",
    "node_validation"
)

# Helper to ensure filesystem integrity at runtime
def initialize_workspace() -> None:
    for directory in PATHS.values():
        directory.mkdir(parents=True, exist_ok=True)

# Immutable mapping for status indicators
STATUS_CODES: Final[dict] = {
    0: "SUCCESS",
    1: "PARTIAL_FAILURE",
    2: "CRITICAL_ABORT"
}

if __name__ == "__main__":
    initialize_workspace()