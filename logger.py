import sys
from datetime import datetime
from pathlib import Path

class CreativeLogger:
    def __init__(self, log_path: str = "automation.log"):
        self.log_file = Path(log_path)
        self._buffer = []

    def __call__(self, message: str, level: str = "INFO") -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {level:^7} | {message}"
        self._buffer.append(entry)
        self._flush()

    def _flush(self):
        while self._buffer:
            msg = self._buffer.pop(0)
            with self.log_file.open("a", encoding="utf-8") as f:
                f.write(f"{msg}\n")

    def error(self, message: str):
        self(message, level="ERROR")

    def success(self, message: str):
        self(message, level="SUCCESS")

logger = CreativeLogger()