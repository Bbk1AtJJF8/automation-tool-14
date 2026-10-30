"""Custom exception hierarchy with dynamic context payload capabilities."""

from typing import Any, Dict, Optional, Tuple, Type


class DynamicAutomationError(Exception):
    """Base exception class capable of encapsulating execution state context."""

    def __init__(
        self,
        message: str,
        *args: Any,
        payload: Optional[Dict[str, Any]] = None,
        severity: int = 1,
    ) -> None:
        super().__init__(message, *args)
        self.message: str = message
        self.payload: Dict[str, Any] = payload or {}
        self.severity: int = max(1, min(severity, 5))

    def enrich(self, **kwargs: Any) -> "DynamicAutomationError":
        """Fluidly attaches additional diagnostic key-value pairs to the exception."""
        self.payload.update(kwargs)
        return self

    def formatted_diagnostics(self) -> str:
        """Generates a structured string breakdown of error context."""
        context_str: str = " | ".join(f"{k}={v!r}" for k, v in sorted(self.payload.items()))
        return f"[{self.__class__.__name__}][Severity:{self.severity}] {self.message} ({context_str or 'No payload'})"


class WorkflowInterrupted(DynamicAutomationError):
    """Raised when an automation flow encounters an unrecoverable step block."""

    def __init__(
        self,
        step_name: str,
        reason: str,
        state_dump: Optional[Dict[str, Any]] = None,
    ) -> None:
        merged_payload: Dict[str, Any] = {"failed_step": step_name, **(state_dump or {})}
        super().__init__(f"Step '{step_name}' halted execution: {reason}", payload=merged_payload, severity=3)


class ResourceThrottledError(DynamicAutomationError):
    """Raised when automation trigger exceeds rate limits or quota boundaries."""

    def __init__(
        self,
        resource_id: str,
        cooldown_seconds: float,
        limit_meta: Optional[Tuple[int, int]] = None,
    ) -> None:
        info: Dict[str, Any] = {"resource": resource_id, "cooldown": cooldown_seconds}
        if limit_meta:
            info["rate_limit"] = f"{limit_meta[0]}/{limit_meta[1]}s"
        super().__init__(
            f"Resource '{resource_id}' throttled. Cooldown required: {cooldown_seconds}s",
            payload=info,
            severity=2,
        )


def escalate_exception(
    exc: Exception, target_type: Type[DynamicAutomationError], **extra_context: Any
) -> DynamicAutomationError:
    """Wraps generic exceptions into specialized automation errors with attached metadata."""
    new_exc = target_type(str(exc))
    return new_exc.enrich(original_type=exc.__class__.__name__, **extra_context)
