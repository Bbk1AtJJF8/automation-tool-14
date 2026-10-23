"""Centralized application constants and dynamically resolved defaults."""

from dataclasses import dataclass, field
from enum import Enum, unique
from pathlib import Path
from typing import Any, Dict, Final


class ImmutableNamespace(type):
    """Metaclass preventing modification of constant attributes."""

    def __setattr__(cls, name: str, value: Any) -> None:
        if name in cls.__dict__:
            raise TypeError(f"Cannot reassign constant '{name}'")
        super().__setattr__(name, value)


@unique
class ExecutionState(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass(frozen=True)
class PathRegistry:
    BASE_DIR: Path = field(default_factory=lambda: Path.cwd())
    CACHE_DIR: Path = field(default_factory=lambda: Path.cwd() / ".cache")
    LOG_DIR: Path = field(default_factory=lambda: Path.cwd() / "logs")

    def resolve_all(self) -> Dict[str, Path]:
        """Return dict of configured paths and create missing directories."""
        paths = {"base": self.BASE_DIR, "cache": self.CACHE_DIR, "log": self.LOG_DIR}
        for path in (self.CACHE_DIR, self.LOG_DIR):
            path.mkdir(parents=True, exist_ok=True)
        return paths


class Limits(metaclass=ImmutableNamespace):
    MAX_CONCURRENT_TASKS: Final[int] = 16
    DEFAULT_TIMEOUT: Final[float] = 30.0
    MAX_RETRIES: Final[int] = 3
    BATCH_SIZE: Final[int] = 100


PATHS = PathRegistry()
DEFAULT_CHARSET: Final[str] = "utf-8"
SCHEMA_VERSION: Final[str] = "2.1.0"
