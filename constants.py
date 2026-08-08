from typing import Final, List, Tuple

# Constants for application configuration

BASE_URL: Final[str] = "https://api.example.com/"

# API endpoints
API_ENDPOINTS: Final[Tuple[str, str]] = (
    "get_items",
    "create_item",
)

# Status codes
class HttpStatus:
    SUCCESS: Final[int] = 200
    CREATED: Final[int] = 201
    NOT_FOUND: Final[int] = 404
    SERVER_ERROR: Final[int] = 500

# Default pagination settings
DEFAULT_PAGE_SIZE: Final[int] = 20
DEFAULT_SORT_ORDER: Final[str] = "asc"

# List of supported file formats
SUPPORTED_FORMATS: Final[List[str]] = ["json", "xml", "csv"]

# Application settings
class AppSettings:
    MAX_CONNECTIONS: Final[int] = 10
    TIMEOUT: Final[int] = 30  # in seconds
    RETRY_ATTEMPTS: Final[int] = 3

