from typing import Callable, Any, List, Dict, Tuple
import functools


class StepFrame:
    __slots__ = ('func', 'name', 'hash_id')

    def __init__(self, name: str, func: Callable):
        self.name = name
        self.func = func
        self.hash_id = id(func)


class FastPipeline:
    """High-performance automation pipeline using inline step memoization."""

    __slots__ = ('_frames', '_cache', '_hits', '_misses')

    def __init__(self) -> None:
        self._frames: List[StepFrame] = []
        self._cache: Dict[Tuple[int, int], Dict[str, Any]] = {}
        self._hits = 0
        self._misses = 0

    def add_step(self, name: str, func: Callable) -> 'FastPipeline':
        self._frames.append(StepFrame(name, func))
        return self

    def execute_batch(self, batch: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Executes pipeline steps over a workload using state hashing."""
        results: List[Dict[str, Any]] = []
        cache = self._cache

        for item in batch:
            data = item.copy()
            for frame in self._frames:
                # Construct state signature from dict items
                state_hash = hash(frozenset(data.items()))
                cache_key = (frame.hash_id, state_hash)

                if cache_key in cache:
                    data = cache[cache_key]
                    self._hits += 1
                else:
                    data = frame.func(data)
                    cache[cache_key] = data
                    self._misses += 1
            results.append(data)
        return results

    def clear_cache(self) -> None:
        self._cache.clear()

    @property
    def cache_hit_ratio(self) -> float:
        total = self._hits + self._misses
        return round((self._hits / total), 4) if total > 0 else 0.0
