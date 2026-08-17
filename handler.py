import logging
from queue import Queue
from threading import Thread

class TaskHandler:
    def __init__(self, num_workers):
        self.tasks = Queue()
        self.workers = []
        for _ in range(num_workers):
            worker = Thread(target=self.process_tasks)
            worker.start()
            self.workers.append(worker)

    def add_task(self, task):
        self.tasks.put(task)

    def process_tasks(self):
        while True:
            task = self.tasks.get()
            if task is None:
                break
            self.execute_task(task)
            self.tasks.task_done()

    def execute_task(self, task):
        logging.info(f'Processing task: {task}')
        # Simulate task processing

    def wait_completion(self):
        self.tasks.join()
        for _ in self.workers:
            self.tasks.put(None)
        for worker in self.workers:
            worker.join()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    handler = TaskHandler(num_workers=3)
    for i in range(10):
        handler.add_task(f'Task {i}')
    handler.wait_completion()