import os
import shutil
from pathlib import Path
from typing import List, Callable

class AutomationEngine:
    def __init__(self, target_dir: str):
        self.root = Path(target_dir)
        self.registry = {}

    def register_action(self, ext: str, func: Callable[[Path], None]):
        self.registry[ext] = func

    def execute_cleanup(self):
        if not self.root.exists():
            return
        
        for item in self.root.iterdir():
            if item.is_file() and item.suffix in self.registry:
                self.registry[item.suffix](item)

def move_to_archive(file_path: Path):
    archive_dir = file_path.parent / "archive"
    archive_dir.mkdir(exist_ok=True)
    shutil.move(str(file_path), str(archive_dir / file_path.name))

def main():
    engine = AutomationEngine("./data")
    engine.register_action(".tmp", lambda p: p.unlink())
    engine.register_action(".log", move_to_archive)
    
    try:
        engine.execute_cleanup()
    except Exception as e:
        print(f"Execution error: {e}")

if __name__ == "__main__":
    main()