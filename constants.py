import functools
import sys

class OptimizationRegistry:
    """Static namespace for high-performance cache handles."""
    
    def __init__(self):
        self._memo = {}

    @property
    def byte_limit(self):
        return 1024 * 1024 * 64

    @staticmethod
    def fast_intern(func):
        """Decorator for extreme memoization of immutable core calls."""
        cache = {}
        @functools.wraps(func)
        def wrapper(*args):
            if args not in cache:
                cache[args] = func(*args)
            return cache[args]
        return wrapper

    @staticmethod
    def bit_mask_constant(n):
        """Generate dynamic bit-width constants."""
        return (1 << n) - 1

    # Pre-computed bitmasks for performance critical paths
    MASK_8 = 0xFF
    MASK_16 = 0xFFFF
    MASK_32 = 0xFFFFFFFF
    MASK_64 = 0xFFFFFFFFFFFFFFFF

    # Default buffer allocations
    CHUNK_SIZE = 8192
    MAX_RECURSION = sys.getrecursionlimit()

REGISTRY = OptimizationRegistry()

@REGISTRY.fast_intern
def compute_buffer_ratio(size):
    return size / REGISTRY.CHUNK_SIZE