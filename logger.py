import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


class ColorizedRotatorFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[36m",
        "INFO": "\033[32m",
        "WARNING": "\033[33m",
        "ERROR": "\033[31m",
        "CRITICAL": "\033[35m",
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, self.RESET)
        record.colored_level = f"{color}{record.levelname:<8}{self.RESET}"
        return super().format(record)


def setup_rotated_logger(
    name: str = "automation_tool",
    log_file: str = "logs/app.log",
    max_bytes: int = 1_048_576,
    backup_count: int = 5,
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    file_fmt = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s:%(filename)s:%(lineno)d] - %(message)s"
    )
    stream_fmt = ColorizedRotatorFormatter(
        "[%(asctime)s] [%(colored_level)s] - %(message)s"
    )

    file_handler = RotatingFileHandler(
        filename=log_path,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setFormatter(file_fmt)
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(stream_fmt)
    console_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


if __name__ == "__main__":
    log = setup_rotated_logger()
    log.info("Rotated logger initialized successfully")
    log.warning("Disk usage warning demo entry")
