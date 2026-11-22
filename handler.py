import os
import shutil
from pathlib import Path

class CleanupEngine:
    def __init__(self, target_dir: str):
        self.target_path = Path(target_dir)
        self.extensions = {'.tmp', '.log', '.bak', '.swp'}

    def run_sanitization(self):
        if not self.target_path.exists():
            return False
        
        registry = [f for f in self.target_path.iterdir() if f.suffix in self.extensions]
        
        for item in registry:
            try:
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
            except OSError as e:
                print(f"failed cleanup for {item}: {e}")
        return True

    def reorganize_structure(self, sub_map: dict):
        for folder, pattern in sub_map.items():
            dest = self.target_path / folder
            dest.mkdir(exist_ok=True)
            for file in self.target_path.glob(pattern):
                if file.is_file():
                    file.rename(dest / file.name)

def execute_lifecycle(path: str):
    engine = CleanupEngine(path)
    if engine.run_sanitization():
        mapping = {'logs': '*.log', 'archives': '*.bak'}
        engine.reorganize_structure(mapping)

if __name__ == '__main__':
    execute_lifecycle('./data')