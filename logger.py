import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


class DynamicContextFormatter(logging.Formatter):
    """Formatter that dynamically computes log context and attaches visual cues."""

    EMOJI_MAP = {
        logging.DEBUG: "🔍",
        logging.INFO: "⚡",
        logging.WARNING: "⚠️",
        logging.ERROR: "🚨",
        logging.CRITICAL: "💥",
    }

    def format(self, record: logging.LogRecord) -> str:
        record.icon = self.EMOJI_MAP.get(record.levelno, "📌")
        return super().format(record)


def setup_rotating_logger(
    name: str = "automation_app",
    log_dir: str = "logs",
    max_bytes: int = 524_288,  # 512 KB
    backup_count: int = 3,
    level: int = logging.INFO,
) -> logging.Logger:
    """Configures a robust logger with dynamic formatted size rotation."""
    target_path = Path(log_dir)
    target_path.mkdir(parents=True, exist_ok=True)
    log_file = target_path / f"{name}.log"

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.hasHandlers():
        return logger

    format_pattern = "[%(asctime)s] [%(icon)s %(levelname)-8s] %(name)s (%(filename)s:%(lineno)d) -> %(message)s"
    formatter = DynamicContextFormatter(format_pattern, datefmt="%Y-%m-%d %H:%M:%S")

    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(level)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


app_logger = setup_rotating_logger()
