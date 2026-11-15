import os
import shutil
from typing import List, Union
from pathlib import Path

def purge_temp_artifacts(target_dirs: List[Union[str, Path]], extensions: tuple = ('.tmp', '.log', '.bak')) -> dict:
    """Aggressive cleanup of stale ephemeral artifacts."""
    report = {'deleted': 0, 'errors': 0}
    for directory in target_dirs:
        path = Path(directory)
        if not path.exists():
            continue
        for item in path.rglob('*'):
            if item.suffix in extensions:
                try:
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
                    report['deleted'] += 1
                except (OSError, PermissionError):
                    report['errors'] += 1
    return report

def structural_cleanup(base_path: str, manifest: List[str]) -> None:
    """Reorganization of project directory structure."""
    root = Path(base_path)
    for entry in manifest:
        target = root / entry
        if target.exists() and target.is_dir():
            archive_target = root / 'archive' / entry
            archive_target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(target), str(archive_target))

class CleanupContext:
    """Context manager for lifecycle resource reclamation."""
    def __init__(self, target: str):
        self.target = Path(target)
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.target.exists():
            shutil.rmtree(self.target)