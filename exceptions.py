class AutomationError(Exception):
    """Base exception class for automation-tool-14"""
    pass

class ConfigurationError(AutomationError):
    """Raised when config validation fails"""
    pass

class ExecutionError(AutomationError):
    """Raised during core logic failures"""
    pass

class ResourceExhaustionError(AutomationError):
    """Raised when system limits are reached"""
    pass

def raise_with_context(exc_class, message, context=None):
    """Creative factory for contextual exceptions"""
    error = exc_class(f"{message} | Context: {context or 'N/A'}")
    setattr(error, 'meta', context)
    raise error

class ExceptionManager:
    """Centralized handler for exception reporting"""
    def __init__(self):
        self.history = []

    def capture(self, e):
        self.history.append({'type': type(e).__name__, 'msg': str(e)})
        return True

    def clear(self):
        self.history = []