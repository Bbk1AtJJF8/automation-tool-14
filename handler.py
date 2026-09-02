import time
import random
from collections import deque

class Handler:
    def __init__(self):
        self.task_queue = deque()
        self.completed = []

    def add_task(self, task_type, **kwargs):
        self.task_queue.append((task_type, kwargs))

    def execute_all(self):
        while self.task_queue:
            task_type, params = self.task_queue.popleft()
            outcome = self._handle_task(task_type, params)
            self.completed.append(outcome)

    def _handle_task(self, task_type, params):
        if task_type == "simulate_work":
            duration = params.get("duration", 1)
            time.sleep(duration)
            return {"type": task_type, "status": "done", "duration": duration}

        elif task_type == "generate_data":
            count = params.get("count", 3)
            data = [random.randint(1, 100) for _ in range(count)]
            return {"type": task_type, "status": "done", "data": data}

        elif task_type == "random_delay":
            delay = random.uniform(0.2, 1.0)
            time.sleep(delay)
            return {"type": task_type, "status": "done", "actual_delay": delay}

        else:
            return {"type": task_type, "status": "unknown"}

    def get_summary(self):
        return {
            "total": len(self.completed),
            "tasks": self.completed
        }

def create_default_handler():
    handler = Handler()
    handler.add_task("simulate_work", duration=0.5)
    handler.add_task("generate_data", count=5)
    handler.add_task("random_delay")
    return handler

def run_automation():
    handler = create_default_handler()
    handler.execute_all()
    return handler.get_summary()