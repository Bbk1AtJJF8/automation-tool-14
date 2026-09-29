import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


class MicrosecondRotator(RotatingFileHandler):
    """Custom file handler appending execution timestamp meta to rotations."""

    def doRollover(self):
        super().doRollover()
        if self.stream:
            self.stream.write("--- LOG ROTATION BOUNDARY MET ---\n")
            self.stream.flush()


def setup_logger(
    name: str = "automation_tool",
    log_filename: str = "automation.log",
    max_bytes: int = 1_048_576,
    backup_count: int = 5,
) -> logging.Logger:
    log_path = Path("logs")
    log_path.mkdir(parents=True, exist_ok=True)
    target_file = log_path / log_filename

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        logger.handlers.clear()

    file_handler = MicrosecondRotator(
        target_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    file_formatter = logging.Formatter(
        "[%(asctime)s.%(msecs)03d] [%(levelname)s] (%(filename)s:%(lineno)d) -> %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = logging.Formatter("⚡ %(levelname)-8s :: %(message)s")
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


app_logger = setup_logger()
