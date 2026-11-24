import datetime
import sys
import os

class CustomLogger:
    def __init__(self, name: str = 'automation-tool-14'):
        self.name = name
        self.log_file = f"{name}.log"

    def _format(self, level: str, message: str) -> str:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return f"[{timestamp}] [{level.upper()}] {message}"

    def info(self, msg: str) -> None:
        self._write('INFO', msg)

    def error(self, msg: str) -> None:
        self._write('ERROR', msg, target=sys.stderr)

    def _write(self, level: str, msg: str, target=sys.stdout) -> None:
        formatted = self._format(level, msg)
        print(formatted, file=target)
        try:
            with open(self.log_file, 'a') as f:
                f.write(formatted + '\n')
        except IOError:
            pass

def get_logger(name: str = 'automation-tool-14') -> CustomLogger:
    return CustomLogger(name)