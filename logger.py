import sys
import datetime
from typing import Any, NoReturn

def log_message(level: str, message: str, meta: dict[str, Any] | None = None) -> None:
    """Dispatch formatted log entry to standard error stream."""
    timestamp: str = datetime.datetime.now().isoformat()
    context: str = f" | {meta}" if meta else ""
    formatted: str = f"[{timestamp}] {level.upper()}: {message}{context}"
    print(formatted, file=sys.stderr)

class TraceBuffer:
    """Ephemeral memory-based log interceptor for unexpected code paths."""
    def __init__(self, limit: int = 10) -> None:
        self._stack: list[str] = []
        self._limit: int = limit

    def capture(self, entry: str) -> None:
        """Append event and enforce cyclic buffer constraints."""
        self._stack.append(f"{datetime.datetime.now()}: {entry}")
        if len(self._stack) > self._limit:
            self._stack.pop(0)

    def dump(self) -> list[str]:
        """Return current buffered state as ordered list."""
        return self._stack

def critical_abort(reason: str) -> NoReturn:
    """Instant process termination with final log broadcast."""
    log_message("CRITICAL", reason)
    sys.exit(1)