from typing import Any, Callable, Dict, List, Union


class StreamProcessor:
    """A fluent pipeline wrapper for nested structural data transformations."""

    def __init__(self, data: Any):
        self._data = data

    def __or__(self, step: Callable[[Any], Any]) -> "StreamProcessor":
        return StreamProcessor(step(self._data))

    def unwrap(self) -> Any:
        return self._data


def flatten_nested_data(
    data: Union[Dict[str, Any], List[Any]], prefix: str = ""
) -> Dict[str, Any]:
    flat = {}
    if isinstance(data, dict):
        for key, val in data.items():
            new_key = f"{prefix}.{key}" if prefix else str(key)
            if isinstance(val, (dict, list)):
                flat.update(flatten_nested_data(val, prefix=new_key))
            else:
                flat[new_key] = val
    elif isinstance(data, list):
        for idx, val in enumerate(data):
            new_key = f"{prefix}[{idx}]"
            if isinstance(val, (dict, list)):
                flat.update(flatten_nested_data(val, prefix=new_key))
            else:
                flat[new_key] = val
    return flat


def coerce_leaf_types(data: Dict[str, Any]) -> Dict[str, Any]:
    coerced = {}
    for k, v in data.items():
        if isinstance(v, str):
            if v.isdigit():
                coerced[k] = int(v)
            elif v.replace(".", "", 1).isdigit() and v.count(".") == 1:
                coerced[k] = float(v)
            elif v.lower() in ("true", "false"):
                coerced[k] = v.lower() == "true"
            else:
                coerced[k] = v
        else:
            coerced[k] = v
    return coerced


def execute_data_pipeline(raw_payload: Dict[str, Any]) -> Dict[str, Any]:
    pipeline = (
        StreamProcessor(raw_payload) | flatten_nested_data | coerce_leaf_types
    )
    return pipeline.unwrap()
