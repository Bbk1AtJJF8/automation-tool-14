from typing import Final, Dict, Any
import os

# Configuration constants for automation-tool-14

TIMEOUT_SECONDS: Final[int] = 30
MAX_RETRIES: Final[int] = 3

DEFAULT_HEADERS: Final[Dict[str, str]] = {
    "User-Agent": "automation-tool-14/1.0",
    "Accept": "application/json"
}

ENV_PREFIX: Final[str] = "AUTO14_"

def get_env_or_default(key: str, default: Any) -> Any:
    """
    Retrieve environment variable with a graceful fallback mechanism.

    :param key: The suffix of the environment variable to look up.
    :param default: The value to return if the environment variable is missing.
    :return: The environment value cast to the type of the default, or the default.
    """
    raw_value: str | None = os.getenv(f"{ENV_PREFIX}{key.upper()}")
    if raw_value is None:
        return default
    
    # Attempt type casting based on default type
    try:
        return type(default)(raw_value)
    except (ValueError, TypeError):
        return default

# Dynamic runtime configuration storage
RUNTIME_CONFIG: Final[Dict[str, Any]] = {
    "debug_mode": get_env_or_default("DEBUG", False),
    "base_url": get_env_or_default("URL", "https://api.automation.internal")
}