import re
from typing import Any, Callable, Dict, List, Union


class MorphingData:
    """Fluid data wrapper enabling dot-path access, regex search, and operator piping."""

    def __init__(self, data: Any):
        self._data = data

    def __getitem__(self, path: str) -> "MorphingData":
        keys = path.split(".")
        curr = self._data
        for k in keys:
            if isinstance(curr, dict) and k in curr:
                curr = curr[k]
            elif isinstance(curr, (list, tuple)) and k.isdigit():
                idx = int(k)
                curr = curr[idx] if 0 <= idx < len(curr) else None
            else:
                return MorphingData(None)
        return MorphingData(curr)

    def __rshift__(self, func: Callable[[Any], Any]) -> "MorphingData":
        """Overload >> operator for transformation piping across scalar or collection values."""
        if self._data is None:
            return self
        if isinstance(self._data, (list, set, tuple)):
            return MorphingData([func(item) for item in self._data])
        return MorphingData(func(self._data))

    def find_keys(self, pattern: str) -> Dict[str, Any]:
        """Recursively extract entries matching a key regex pattern."""
        results = {}
        regex = re.compile(pattern)

        def _search(curr: Any, prefix: str = ""):
            if isinstance(curr, dict):
                for k, v in curr.items():
                    full_key = f"{prefix}.{k}" if prefix else str(k)
                    if regex.search(str(k)):
                        results[full_key] = v
                    _search(v, full_key)
            elif isinstance(curr, (list, tuple)):
                for i, item in enumerate(curr):
                    _search(item, f"{prefix}[{i}]")

        _search(self._data)
        return results

    def unwrap(self, default: Any = None) -> Any:
        return self._data if self._data is not None else default

    def __repr__(self) -> str:
        return f"MorphingData({repr(self._data)})"
