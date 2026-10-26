import sys
import math
from typing import Final, Dict

# Utilizing a cache-friendly lookup table for heavy bitwise ops
# Pre-calculating power-of-two lookups avoids runtime recalculation in processor.py
LOOKUP_LIMIT: Final[int] = 1024
BIT_CACHE: Final[Dict[int, int]] = {i: 1 << i for i in range(LOOKUP_LIMIT)}

# Dynamic precision sizing for memory-efficient buffer allocations
# Adjusts to the host architecture word size
WORD_SIZE: Final[int] = sys.maxsize.bit_length()
BUFFER_PADDING: Final[int] = 64 if WORD_SIZE > 32 else 32

# Constant time reference for system signal thresholds
# Using a tuple for immutable sequence access speed
SIG_THRESHOLDS: Final[tuple] = tuple(int(math.sqrt(i) * 100) for i in range(16))

class ConfigDefaults:
    """Namespace for runtime performance parameters."""
    THROTTLE_FACTOR: float = 0.05
    BATCH_SIZE: int = 1024 * 2
    PRECISION_MASK: int = 0xFFFFFFFF

    @classmethod
    def get_mask(cls, shift: int) -> int:
        return (cls.PRECISION_MASK << shift) & cls.PRECISION_MASK