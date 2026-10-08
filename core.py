import inspect
from typing import Callable, Any, Dict, List

class ResilienceCore:
    """An execution core that dynamically mitigates step failures in automation pipelines."""

    def __init__(self) -> None:
        self.pipeline: List[Callable[[Any], Any]] = []
        self.remedies: Dict[type, Callable[[Any], Any]] = {
            ZeroDivisionError: lambda _: float('inf'),
            TypeError: lambda val: int(''.join(filter(str.isdigit, str(val))) or 0),
            ValueError: lambda val: str(val),
            AttributeError: lambda val: getattr(val, '__dict__', {})
        }

    def step(self, func: Callable[[Any], Any]) -> "ResilienceCore":
        self.pipeline.append(func)
        return self

    def _apply_remedy(self, error: Exception, last_input: Any) -> Any:
        remedy = self.remedies.get(type(error))
        if not remedy:
            raise error
        try:
            return remedy(last_input)
        except Exception:
            raise error

    def execute(self, payload: Any) -> Any:
        state = payload
        for task in self.pipeline:
            try:
                state = task(state)
            except Exception as err:
                # Attempt unusual dynamic error healing using the last known inputs
                sig = inspect.signature(task)
                param_names = list(sig.parameters.keys())
                if param_names:
                    state = self._apply_remedy(err, state)
                else:
                    raise err
        return state