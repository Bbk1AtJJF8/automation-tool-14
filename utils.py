from typing import Any, Callable, Dict, List, Union


class FlowData:
    """A wrapper around nested data structures enabling fluid pipeline transformations."""

    def __init__(self, data: Any):
        self.raw = data

    def select(self, *path_parts: str) -> "FlowData":
        current = self.raw
        for part in path_parts:
            if isinstance(current, dict):
                current = current.get(part)
            elif isinstance(current, (list, tuple)) and part.isdigit():
                idx = int(part)
                current = current[idx] if 0 <= idx < len(current) else None
            else:
                return FlowData(None)
        return FlowData(current)

    def mutate(self, transform_fn: Callable[[Any], Any]) -> "FlowData":
        if self.raw is None:
            return FlowData(None)
        return FlowData(transform_fn(self.raw))

    def flatten(self, parent_key: str = "", sep: str = ".") -> Dict[str, Any]:
        items: List[tuple] = []
        if isinstance(self.raw, dict):
            for k, v in self.raw.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else str(k)
                if isinstance(v, dict):
                    items.extend(FlowData(v).flatten(new_key, sep=sep).items())
                else:
                    items.append((new_key, v))
        return dict(items)

    def __rshift__(self, fn: Callable[[Any], Any]) -> "FlowData":
        return self.mutate(fn)

    def __repr__(self) -> str:
        return f"<FlowData payload={repr(self.raw)}>"


def process_payload(
    data: Union[dict, list], path: str, transform_fn: Callable = None
) -> Any:
    flow = FlowData(data)
    flow = flow.select(*path.split("."))
    if transform_fn:
        flow = flow >> transform_fn
    return flow.raw
