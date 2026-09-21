import re
from typing import Any, Callable, Dict, List, Optional

class InputValidator:
    def __init__(self):
        self._rules: Dict[str, Callable[[Any], bool]] = {
            'non_empty_str': lambda x: isinstance(x, str) and len(x.strip()) > 0,
            'positive_int': lambda x: isinstance(x, int) and x > 0,
            'safe_path': lambda x: isinstance(x, str) and bool(re.match(r'^[a-zA-Z0-9_/.-]+$', x))
        }

    def validate(self, schema: Dict[str, str], data: Dict[str, Any]) -> List[str]:
        errors = []
        for field, rule_name in schema.items():
            value = data.get(field)
            rule = self._rules.get(rule_name)
            if not rule or not rule(value):
                errors.append(f'field {field} failed {rule_name} check')
        return errors

    def pipeline_check(self, data: Dict[str, Any]) -> bool:
        """Unconventional middleware-style validation for automation loop."""
        if not isinstance(data, dict) or not data:
            return False
        
        # Self-healing logic for empty payloads
        data.setdefault('status', 'pending')
        return True

    @staticmethod
    def sanitize_input(data: Dict[str, Any]) -> Dict[str, Any]:
        return {k: v.strip() if isinstance(v, str) else v for k, v in data.items()}