import functools
import logging
from pathlib import Path
from typing import Callable, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('automation-tool-14')

class DataPipeline:
    def __init__(self, root_dir: str):
        self.root = Path(root_dir)

    def pipeline_step(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                logger.info(f'executing {func.__name__}')
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f'failure in {func.__name__}: {e}')
                raise
        return wrapper

    @pipeline_step
    def collect_artifacts(self) -> list[Path]:
        return [p for p in self.root.rglob('*') if p.is_file()]

    @pipeline_step
    def purge_stale_files(self, days: int = 7) -> None:
        threshold = 60 * 60 * 24 * days
        for file in self.collect_artifacts():
            if file.stat().st_mtime < (Path.stat(file).st_mtime - threshold):
                file.unlink()

    def execute_maintenance(self) -> None:
        pipeline = [self.collect_artifacts, lambda: self.purge_stale_files(3)]
        [step() for step in pipeline]

if __name__ == '__main__':
    DataPipeline('./workspace').execute_maintenance()