from typing import Any, Callable, Dict, List, Union

def cast_structure(data: Any, schema: Dict[str, Callable]) -> Dict[str, Any]:
    """Transforms input dict values via schema-defined casting functions."""
    return {k: schema[k](v) if k in schema else v for k, v in data.items()}

def recursive_sanitize(data: Any, target_type: type = str, replacement: str = "") -> Any:
    """Recursively cleans dictionary or list elements of a specific type."""
    if isinstance(data, dict):
        return {k: recursive_sanitize(v, target_type, replacement) for k, v in data.items()}
    elif isinstance(data, list):
        return [recursive_sanitize(i, target_type, replacement) for i in data]
    return replacement if isinstance(data, target_type) else data

def batch_validate(items: List[Any], predicate: Callable[[Any], bool]) -> Dict[str, List[Any]]:
    """Categorizes data points by predicate truthiness using dictionary comprehension."""
    results = {"valid": [], "invalid": []}
    [results["valid" if predicate(x) else "invalid"].append(x) for x in items]
    return results

def deep_freeze(data: Any) -> Union[tuple, frozenset, Any]:
    """Converts mutable data structures into immutable variants for hashing."""
    if isinstance(data, list):
        return tuple(deep_freeze(i) for i in data)
    elif isinstance(data, dict):
        return frozenset((k, deep_freeze(v)) for k, v in data.items())
    return data