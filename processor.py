import functools
from typing import Callable, Any, List, Dict, Tuple

class ReorganizedPipeline:
    """Self-organizing task pipeline with automated cleanup context."""

    def __init__(self) -> None:
        self._stages: List[Tuple[int, Callable[..., Any]]] = []
        self._cleanups: List[Callable[[], None]] = []

    def stage(self, priority: int = 10, defer_cleanup: Callable[[], None] | None = None):
        def decorator(fn: Callable[..., Any]):
            @functools.wraps(fn)
            def wrapped(*args, **kwargs):
                if defer_cleanup:
                    self._cleanups.append(defer_cleanup)
                return fn(*args, **kwargs)

            self._stages.append((priority, wrapped))
            self._stages.sort(key=lambda x: x[0])
            return wrapped
        return decorator

    def __call__(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        state = payload.copy()
        try:
            for _, stage_func in self._stages:
                res = stage_func(state)
                if isinstance(res, dict):
                    state.update(res)
        finally:
            self.flush()
        return state

    def flush(self) -> None:
        while self._cleanups:
            clean_step = self._cleanups.pop()
            try:
                clean_step()
            except Exception:
                pass


pipeline = ReorganizedPipeline()

@pipeline.stage(priority=1, defer_cleanup=lambda: None)
def normalize_payload(ctx: Dict[str, Any]) -> Dict[str, Any]:
    raw = ctx.get("input", "")
    return {"normalized": str(raw).strip().lower()}

@pipeline.stage(priority=2)
def extract_metadata(ctx: Dict[str, Any]) -> Dict[str, Any]:
    norm = ctx.get("normalized", "")
    return {"length": len(norm), "words": norm.split()}

def run_processor(data: Dict[str, Any]) -> Dict[str, Any]:
    return pipeline(data)
