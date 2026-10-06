import sys
import datetime
from typing import Any

class ColorfulLogger:
    COLORS = {
        "INFO": "\033[94m",
        "WARN": "\033[93m",
        "ERROR": "\033[91m",
        "RESET": "\033[0m"
    }

    @staticmethod
    def _format(level: str, message: str) -> str:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        color = ColorfulLogger.COLORS.get(level, "")
        return f"{color}[{timestamp}] {level}: {message}{ColorfulLogger.COLORS['RESET']}"

    def info(self, msg: Any) -> None:
        print(self._format("INFO", str(msg)))

    def warn(self, msg: Any) -> None:
        print(self._format("WARN", str(msg)), file=sys.stderr)

    def error(self, msg: Any) -> None:
        print(self._format("ERROR", str(msg)), file=sys.stderr)

def get_logger() -> ColorfulLogger:
    return ColorfulLogger()

if __name__ == "__main__":
    log = get_logger()
    log.info("System initialized")
    log.warn("Memory usage creeping up")
    log.error("Automation sequence failed")