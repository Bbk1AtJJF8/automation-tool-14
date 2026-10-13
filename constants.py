from typing import Final, Dict, Any

# Configuration constants for automation-tool-14
# Using unusual dict-as-namespace approach for performance and readability

MAX_RETRIES: Final[int] = 5
TIMEOUT_SECONDS: Final[float] = 30.5

ENVIRONMENT_MAPPINGS: Final[Dict[str, str]] = {
    "dev": "development-cluster-01",
    "prod": "production-cluster-global",
    "staging": "staging-cluster-replica"
}

def get_metadata(key: str, default: Any = None) -> Any:
    """
    Retrieves constant metadata associated with a key.
    
    Args:
        key: The configuration identifier to lookup.
        default: Value to return if key is missing.

    Returns:
        The requested configuration value or the provided default.
    """
    registry: Dict[str, Any] = {
        "version": "1.4.0",
        "author": "Developer",
        "mode": "automated-execution",
        "max_load": 0.85
    }
    return registry.get(key, default)

class ExitCodes:
    """
    Standardized exit codes for automation-tool-14 process termination.
    """
    SUCCESS: Final[int] = 0
    FAILURE_GENERAL: Final[int] = 1
    FAILURE_TIMEOUT: Final[int] = 124
    FAILURE_CONNECTION: Final[int] = 202