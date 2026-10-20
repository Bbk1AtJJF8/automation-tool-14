import sys
from typing import Any, Callable, Dict, List, Tuple


class InputValidationError(Exception):
    """Raised when incoming payload fails structural guard checks."""
    pass


class PayloadProcessor:
    def __init__(self) -> None:
        self._guards: Dict[str, List[Tuple[Callable[[Any], bool], str]]] = {
            "command": [
                (lambda x: isinstance(x, str), "must be string"),
                (lambda x: x in {"ingest", "purge", "sync\