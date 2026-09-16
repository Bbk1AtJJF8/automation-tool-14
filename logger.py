import time
import threading
from collections import deque

class AsyncBufferLogger:
    def __init__(self, capacity=1000):
        self.buffer = deque(maxlen=capacity)
        self.lock = threading.Lock()
        self._running = True
        self.worker = threading.Thread(target=self._flush, daemon=True)
        self.worker.start()

    def log(self, message):
        self.buffer.append(f"[{time.time():.4f}] {message}")

    def _flush(self):
        while self._running:
            if self.buffer:
                batch = list(self.buffer)
                self.buffer.clear()
                with open("app.log", "a") as f:
                    f.write("\n".join(batch) + "\n")
            time.sleep(0.5)

    def shutdown(self):
        self._running = False
        self.worker.join()

logger = AsyncBufferLogger()