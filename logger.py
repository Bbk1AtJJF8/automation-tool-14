import sys
import time
from functools import wraps
from typing import Any, Callable, List, Optional, TextIO


class PrismLogger:
    """A vivid contextual logger using dynamic ANSI color spectrum allocation.

    Transforms log entries into color-coded streams anchored to calling scope metadata.
    """

    _SPECTRUM: List[str] = [
        "\033[36m",  # Cyan
        "\033[32m",  # Green
        "\033[33m",  # Yellow
        "\033[35m",  # Magenta
        "\033[34m",  # Blue
    ]
    _RESET: str = "\033[0m"

    def __init__(self, stream: Optional[TextIO] = None, enable_color: bool = True) -> None:
        """Initialize logger bound to a specific text output stream."""
        self.stream: TextIO = stream or sys.stdout
        self.enable_color: bool = enable_color

    def _chroma(self, text: str, hash_key: int) -> str:
        """Apply deterministic color gradient based on string hash key."""
        if not self.enable_color:
            return text
        color: str = self._SPECTRUM[hash_key % len(self._SPECTRUM)]
        return f"{color}{text}{self._RESET}"

    def emit(self, level: str, message: str, **extra: Any) -> None:
        """Write structured payload to destination stream with timestamp context."""
        timestamp: str = time.strftime("%Y-%m-%d %H:%M:%S")
        caller: str = sys._getframe(1).f_code.co_name
        hash_val: int = sum(ord(c) for c in level)

        prefix: str = self._chroma(f"[{timestamp}] [{level.upper()}] [{caller}]", hash_val)
        extra_fmt: str = f" | {extra}" if extra else ""

        self.stream.write(f"{prefix} {message}{extra_fmt}\n")
        self.stream.flush()

    def trace_execution(self, level: str = "INFO") -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Decorator mapping function execution cycles to structured logs."""
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                self.emit(level, f"Entering {func.__name__}")
                start: float = time.perf_counter()
                try:
                    result: Any = func(*args, **kwargs)
                    elapsed: float = (time.perf_counter() - start) * 1000
                    self.emit(level, f"Exited {func.__name__}", duration_ms=round(elapsed, 2))
                    return result
                except Exception as err:
                    self.emit("ERROR", f"Failed {func.__name__}", error=str(err))
                    raise err
            return wrapper
        return decorator


default_logger: PrismLogger = PrismLogger()
