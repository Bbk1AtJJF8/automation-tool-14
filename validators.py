import math
import re
from typing import Any, Callable, Union

class PipelineValidator:
    def __init__(self, step: Callable[[Any], Any]):
        self.step = step

    def __rshift__(self, next_step: "PipelineValidator") -> "PipelineValidator":
        def chain(val: Any) -> Any:
            return next_step.step(self.step(val))
        chain.__name__ = f"{self.step.__name__} -> {next_step.step.__name__}"
        return PipelineValidator(chain)

    def __call__(self, val: Any) -> Any:
        try:
            return self.step(val)
        except Exception as exc:
            raise ValueError(f"Pipeline crashed at [{self.step.__name__}]: {exc}") from exc

def reject_extremes(val: Any) -> Union[int, float]:
    if isinstance(val, str):
        val = val.strip().lower()
        if val in ("nan", "inf", "-inf", "infinity", "-infinity"):
            raise ValueError("unsafe mathematical representation detected")
        try:
            val = float(val) if "." in val else int(val)
        except ValueError as exc:
            raise ValueError(f"conversion failure: {exc}") from exc
    if isinstance(val, (int, float)):
        if math.isnan(val) or math.isinf(val):
            raise ValueError("unsupported float variant")
        return val
    raise ValueError(f"unsupported type {type(val).__name__}")

def purge_hidden_payloads(val: Any) -> str:
    serialized = str(val)
    cleaned = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", serialized)
    if len(cleaned) < len(serialized) / 2:
        raise ValueError("excessive binary control character density")
    return cleaned

def break_cycles(val: Any) -> Any:
    visited = set()
    def _scan(node: Any) -> None:
        if id(node) in visited:
            raise ValueError("malicious circular reference discovered")
        if isinstance(node, (dict, list, set)):
            visited.add(id(node))
            items = node.values() if isinstance(node, dict) else node
            for child in items:
                _scan(child)
            visited.remove(id(node))
    _scan(val)
    return val

numeric_validator = PipelineValidator(break_cycles) >> PipelineValidator(reject_extremes)
payload_sanitizer = PipelineValidator(break_cycles) >> PipelineValidator(purge_hidden_payloads)
