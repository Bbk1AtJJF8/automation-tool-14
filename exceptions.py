import functools
import logging
from typing import Callable, Any

class AutomationError(Exception):
    """Base exception for automation-tool-14."""

class ConfigurationError(AutomationError):
    """Raised when tool configuration is malformed."""

class ExecutionTimeoutError(AutomationError):
    """Raised when an automated task exceeds time limits."""

def suppress_errors(logger: logging.Logger) -> Callable:
    """Decorator for trapping routine automation failures."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Task failed: {type(e).__name__} - {e}")
                return None
        return wrapper
    return decorator

class ErrorFactory:
    """Dynamic generation of context-aware exceptions."""
    @staticmethod
    def raise_contextual(message: str, context: str) -> None:
        full_msg = f"[{context.upper()}] {message}"
        if "config" in context:
            raise ConfigurationError(full_msg)
        raise AutomationError(full_msg)