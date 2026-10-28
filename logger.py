import time
import threading
from collections import deque

class AsyncLogger:
    def __init__(self, buffer_size=1024):
        self._queue = deque(maxlen=buffer_size)
        self._lock = threading.Lock()
        self._flush_interval = 0.5
        self._running = True
        self._worker = threading.Thread(target=self._process, daemon=True)
        self._worker.start()

    def log(self, message: str):
        timestamp = time.strftime('%H:%M:%S')
        self._queue.append(f"[{timestamp}] {message}")

    def _process(self):
        while self._running:
            time.sleep(self._flush_interval)
            if self._queue:
                batch = list(self._queue)
                self._queue.clear()
                with open('automation.log', 'a') as f:
                    f.write('\n'.join(batch) + '\n')

    def shutdown(self):
        self._running = False
        self._worker.join()

logger = AsyncLogger()