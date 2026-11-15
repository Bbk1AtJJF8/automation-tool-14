import re
from typing import Any, Callable, Dict, List, Tuple


class Rule:
    """Chainable validation predicate wrapper."""

    def __init__(self, predicate: Callable[[Any], bool], message: str):
        self.predicate = predicate
        self.message = message

    def __and__(self, other: "Rule") -> "Rule":
        return Rule(
            lambda x: self.predicate(x) and other.predicate(x),
            f"({self.message} & {other.message})"
        )

    def __call__(self, value: Any) -> Tuple[bool, str]:
        ok = bool(self.predicate(value))
        return ok, ("OK" if ok else self.message)


def is_non_empty_str() -> Rule:
    return Rule(lambda v: isinstance(v, str) and len(v.strip()) > 0, "value must be non-empty string")


def matches_regex(pattern: str, desc: str = "custom pattern") -> Rule:
    regex = re.compile(pattern)
    return Rule(lambda v: isinstance(v, str) and bool(regex.search(v)), f"value must match {desc}")


def is_in_range(min_val: float, max_val: float) -> Rule:
    return Rule(lambda v: isinstance(v, (int, float)) and min_val <= v <= max_val, f"value must be in range [{min_val}, {max_val}]")


def validate_dict(data: Dict[str, Any], schema: Dict[str, Rule]) -> Tuple[bool, List[str]]:
    errors = []
    for field, rule in schema.items():
        if field not in data:
            errors.append(f"missing field '{field}'")
            continue
        valid, msg = rule(data[field])
        if not valid:
            errors.append(f"field '{field}': {msg}")
    return len(errors) == 0, errors