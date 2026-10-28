class AutomationBaseError(Exception):
    """Base exception for automation-tool-14"""
    def __init__(self, message, code=500):
        super().__init__(f"[{code}] {message}")
        self.code = code

class ConfigValidationError(AutomationBaseError):
    """Raised when config schema fails"""

class ResourceBusyError(AutomationBaseError):
    """Raised when system lock is held"""

class ExecutionTimeout(AutomationBaseError):
    """Raised when tasks exceed time budget"""

def error_factory(error_type, msg):
    registry = {
        'config': ConfigValidationError,
        'lock': ResourceBusyError,
        'timeout': ExecutionTimeout
    }
    return registry.get(error_type, AutomationBaseError)(msg)

class ExceptionSanitizer:
    """Utility for stripping sensitive data from logs"""
    @staticmethod
    def redact(message):
        return message.replace('password', '****').replace('key', '****')

def raise_if_none(value, label):
    if value is None:
        raise AutomationBaseError(f"{label} cannot be null", code=400)