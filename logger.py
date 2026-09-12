import logging
from typing import Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

class DynamicStateLogger:
    """
    An unusual proxy wrapping dictionary or object payloads to track
    and log every internal mutation or data access point automatically.
    """
    def __init__(self, target: Any, path: str = 'payload'):
        super().__setattr__('_target', target)
        super().__setattr__('_path', path)
        super().__setattr__('_logger', logging.getLogger('StateTracker'))

    def __getattr__(self, name: str) -> Any:
        val = getattr(self._target, name)
        self._logger.info('[ACCESS] %s.%s -> %s', self._path, name, type(val).__name__)
        if isinstance(val, (dict, list, object)) and not isinstance(val, (str, int, float, bool, type(None))):
            return DynamicStateLogger(val, f'{self._path}.{name}')
        return val

    def __setattr__(self, name: str, value: Any) -> None:
        old_val = getattr(self._target, name, None)
        setattr(self._target, name, value)
        self._logger.info('[MUTATE] %s.%s | %r => %r', self._path, name, old_val, value)

    def __getitem__(self, key: Any) -> Any:
        val = self._target[key]
        self._logger.info('[ACCESS] %s[%r] -> %s', self._path, key, type(val).__name__)
        if isinstance(val, (dict, list)):
            return DynamicStateLogger(val, f'{self._path}[{repr(key)}]')
        return val

    def __setitem__(self, key: Any, value: Any) -> None:
        try:
            old_val = self._target[key]
        except (KeyError, IndexError, TypeError):
            old_val = None
        self._target[key] = value
        self._logger.info('[MUTATE] %s[%r] | %r => %r', self._path, key, old_val, value)

    def __repr__(self) -> str:
        return repr(self._target)
