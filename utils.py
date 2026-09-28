from typing import Any, Union, Generator

class DataPathNavigator:
    """A creative way to traverse and manipulate nested dictionary data
    using the division (/) operator, supporting fallback values.
    """
    def __init__(self, data: Any, default: Any = None):
        self.data = data
        self.default = default

    def __truediv__(self, key: Union[str, int]) -> 'DataPathNavigator':
        if self.data is self.default:
            return self

        try:
            if isinstance(self.data, dict) and key in self.data:
                return DataPathNavigator(self.data[key], self.default)
            elif isinstance(self.data, (list, tuple)) and isinstance(key, int):
                if 0 <= key < len(self.data):
                    return DataPathNavigator(self.data[key], self.default)
        except Exception:
            pass
        return DataPathNavigator(self.default, self.default)

    def val(self) -> Any:
        return self.data

    def items_flat(self) -> Generator[tuple[str, Any], None, None]:
        """Flattens nested dictionaries into path-tuples and values."""
        def _flatten(current: Any, path: list[str]) -> Generator[tuple[str, Any], None, None]:
            if isinstance(current, dict):
                for k, v in current.items():
                    yield from _flatten(v, path + [str(k)])
            elif isinstance(current, (list, tuple)):
                for i, v in enumerate(current):
                    yield from _flatten(v, path + [str(i)])
            else:
                yield (".".join(path), current)

        if isinstance(self.data, (dict, list, tuple)):
            yield from _flatten(self.data, [])
        else:
            yield ("", self.data)

def wrap_data(data: Any, default: Any = None) -> DataPathNavigator:
    return DataPathNavigator(data, default)