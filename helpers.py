from typing import Any, Callable, Dict, List, Union

class DataPipe:
    """Fluent pipeline wrapper for nested dictionary navigation and data transformation."""

    def __init__(self, data: Any = None):
        self._data = data

    def __getitem__(self, key: Union[str, int, slice, tuple]) -> "DataPipe":
        if self._data is None:
            return DataPipe(None)
        if isinstance(key, tuple):
            curr = self._data
            for k in key:
                if isinstance(curr, dict):
                    curr = curr.get(k)
                elif isinstance(curr, (list, tuple)) and isinstance(k, int) and 0 <= k < len(curr):
                    curr = curr[k]
                else:
                    return DataPipe(None)
            return DataPipe(curr)
        if isinstance(self._data, dict):
            return DataPipe(self._data.get(key))
        if isinstance(self._data, (list, tuple)) and isinstance(key, (int, slice)):
            try:
                return DataPipe(self._data[key])
            except (IndexError, TypeError):
                return DataPipe(None)
        return DataPipe(None)

    def __or__(self, func: Callable[[Any], Any]) -> "DataPipe":
        """Overloads bitwise OR as a pipeline application operator."""
        if self._data is None:
            return DataPipe(None)
        try:
            return DataPipe(func(self._data))
        except Exception:
            return DataPipe(None)

    def collect(self, default: Any = None) -> Any:
        return self._data if self._data is not None else default

def sanitize_structure(data: Any) -> Any:
    """Recursively normalizes dictionary keys and strips outer spaces."""
    if isinstance(data, dict):
        return {
            str(k).strip().lower().replace("-", "_").replace(" ", "_"): sanitize_structure(v)
            for k, v in data.items()
        }
    if isinstance(data, list):
        return [sanitize_structure(item) for item in data]
    if isinstance(data, str):
        return data.strip()
    return data
