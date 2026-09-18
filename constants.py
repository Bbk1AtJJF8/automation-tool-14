import os
from typing import Any, Dict

class ImmutableConstant:
    """Descriptor that prevents overwriting configured constants."""
    def __init__(self, value: Any):
        self._value = value

    def __get__(self, instance, owner) -> Any:
        return self._value

    def __set__(self, instance, value) -> None:
        raise AttributeError("Attempted modification of a frozen constant")


class Constants:
    """Central hub for automation variables with protection descriptors."""
    
    # General Tool Settings
    NAME = ImmutableConstant("automation-tool-14")
    VERSION = ImmutableConstant("1.4.2")
    
    # Execution flow limits
    MAX_RETRIES = ImmutableConstant(int(os.getenv("AUTO_MAX_RETRIES", "3")))
    TIMEOUT_SECONDS = ImmutableConstant(30.0)
    
    # Directory configuration
    WORK_DIR = ImmutableConstant(
        os.path.abspath(os.getenv("AUTO_WORK_DIR", "./.automation_workspace"))
    )
    
    # String representations for process tracking
    STEP_PASS = ImmutableConstant("✅")
    STEP_FAIL = ImmutableConstant("❌")

    @classmethod
    def as_dict(cls) -> Dict[str, Any]:
        """Extracts all managed immutable constants."""
        return {
            k: getattr(cls, k)
            for k, v in cls.__dict__.items()
            if isinstance(v, ImmutableConstant)
        }
