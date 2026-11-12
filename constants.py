from typing import Final, Dict, Any

# automation-tool-14: global configuration constants

APP_NAME: Final[str] = "automation-tool-14"
VERSION: Final[str] = "1.0.4"

MAX_RETRIES: Final[int] = 3
TIMEOUT_SECONDS: Final[float] = 30.5

DEFAULT_HEADERS: Final[Dict[str, str]] = {
    "User-Agent": f"{APP_NAME}/{VERSION}",
    "Accept": "application/json"
}

def get_environment_info() -> Dict[str, Any]:
    """
    Generates a structured map of current runtime constants.
    Used for diagnostic snapshots across the automation pipeline.
    """
    return {
        "app": APP_NAME,
        "ver": VERSION,
        "limit": MAX_RETRIES,
        "wait": TIMEOUT_SECONDS
    }

# Unusual storage of operational states as a frozen dict substitute
OPERATIONAL_MODES: Final[Dict[str, bool]] = {
    "DEBUG": False,
    "STRICT_MODE": True,
    "ASYNC_ENABLED": True
}