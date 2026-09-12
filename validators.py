"""Dynamic schema validator engine for automation task payloads."""

from typing import Any, Callable, Dict, List, Tuple


class Rule:
    def __init__(self, predicate: Callable[[Any], bool], message: str):
        self.predicate = predicate
        self.message = message

    def __call__(self, value: Any) -> Tuple[bool, str]:
        try:
            passed = bool(self.predicate(value))
            return passed, "" if passed else self.message
        except Exception as err:
            return False, f"evaluation error: {err}"

    def __and__(self, other: "Rule") -> "Rule":
        return Rule(
            lambda v: self(v)[0] and other(v)[0],
            f"({self.message} AND {other.message})",
        )

    def __or__(self, other: "Rule") -> "Rule":
        return Rule(
            lambda v: self(v)[0] or other(v)[0],
            f"({self.message} OR {other.message})",
        )

    def __invert__(self) -> "Rule":
        return Rule(lambda v: not self(v)[0], f"NOT({self.message})")


class Validator:
    def __init__(self, schema: Dict[str, Rule]):
        self._schema = schema

    def validate(self, payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errors = []
        for key, rule in self._schema.items():
            if key not in payload:
                errors.append(f"missing required field '{key}'")
                continue
            ok, msg = rule(payload[key])
            if not ok:
                errors.append(f"field '{key}' failed check: {msg}")
        return len(errors) == 0, errors


is_str = Rule(lambda x: isinstance(x, str), "must be string")
is_int = Rule(lambda x: isinstance(x, int), "must be integer")
is_non_empty = Rule(lambda x: len(x) > 0, "must be non-empty")
is_positive = Rule(lambda x: x > 0, "must be positive")

valid_name = is_str & is_non_empty
valid_port = is_int & is_positive
