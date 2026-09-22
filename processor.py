from typing import List, Union, Callable, Any

class DataProcessor:
    """orchestrates transformation pipelines using functional composition"""

    def __init__(self, transforms: List[Callable[[Any], Any]] = None) -> None:
        self._pipeline: List[Callable[[Any], Any]] = transforms or []

    def process(self, data: Union[str, int, float]) -> Any:
        """applies chained transformations to the input data"""
        result: Any = data
        for step in self._pipeline:
            result = step(result)
        return result

    def add_step(self, func: Callable[[Any], Any]) -> 'DataProcessor':
        """appends a new function to the processing pipeline"""
        self._pipeline.append(func)
        return self

def sanitize(value: Any) -> str:
    """forces input into a stripped string format"""
    return str(value).strip().lower()

def double_it(value: str) -> str:
    """concatenates string with itself"""
    return f"{value}{value}"

if __name__ == "__main__":
    # usage example of the creative pipeline approach
    proc = DataProcessor([sanitize])
    proc.add_step(double_it)
    
    final_output = proc.process("  AutomationTool14  ")
    print(f"Result: {final_output}")