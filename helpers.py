import os
import shutil
from pathlib import Path
from typing import Union, List

class CleanupEngine:
    def __init__(self, target_dir: str = './tmp'):
        self.target = Path(target_dir)

    def purge_stale_artifacts(self, extension: str = '.log') -> int:
        count = 0
        if not self.target.exists():
            return count
        
        for item in self.target.iterdir():
            if item.is_file() and item.suffix == extension:
                try:
                    item.unlink()
                    count += 1
                except OSError:
                    continue
        return count

    def consolidate_structure(self, sub_dirs: List[str]) -> None:
        base = self.target.resolve()
        for sub in sub_dirs:
            path = base / sub
            if path.is_dir():
                for child in path.iterdir():
                    target_path = base / child.name
                    shutil.move(str(child), str(target_path))
                path.rmdir()

def get_directory_health(path: Union[str, Path]) -> dict:
    root = Path(path)
    return {
        'files': sum(1 for f in root.rglob('*') if f.is_file()),
        'size': sum(f.stat().st_size for f in root.rglob('*') if f.is_file())
    }