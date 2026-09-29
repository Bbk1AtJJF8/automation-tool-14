import inspect
from functools import wraps
from typing import Any, Callable, Dict, Sequence


class AutomationContext:
    def __init__(self, **initial_state):
        self._state = dict(initial_state)

    def __getattr__(self, name: str) -> Any:
        return self._state.get(name)

    def update(self, **kwargs) -> "AutomationContext":
        self._state.update(kwargs)
        return self


class TaskRegistry:
    def __init__(self):
        self._tasks: Dict[str, Callable] = {}

    def register(self, name: str | None = None):
        def decorator(func: Callable):
            task_name = name or func.__name__

            @wraps(func)
            def wrapper(ctx: AutomationContext, *args, **kwargs):
                sig = inspect.signature(func)
                bound_kwargs = {}
                for param in sig.parameters.values():
                    if param.name in ctx._state:
                        bound_kwargs[param.name] = ctx._state[param.name]
                bound_kwargs.update(kwargs)
                result = func(ctx, *args, **bound_kwargs)
                if isinstance(result, dict):
                    ctx.update(**result)
                return result

            self._tasks[task_name] = wrapper
            return wrapper

        return decorator

    def execute_pipeline(self, steps: Sequence[str], ctx: AutomationContext | None = None) -> AutomationContext:
        context = ctx or AutomationContext()
        for step in steps:
            if step not in self._tasks:
                raise KeyError(f"Task '{step}' not registered")
            self._tasks[step](context)
        return context


engine = TaskRegistry()


@engine.register("load_source")
def fetch_raw_data(ctx, source_uri="default://stream"):
    return {"raw_payload": [10, 20, 30, 40], "uri": source_uri}


@engine.register("normalize")
def transform_data(ctx, raw_payload):
    scaled = [x * 1.5 for x in raw_payload]
    return {"processed_data": scaled}


def run_default_workflow() -> AutomationContext:
    return engine.execute_pipeline(["load_source", "normalize"])
