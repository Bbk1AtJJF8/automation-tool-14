from typing import Any, Dict, Optional

class AutomationTool:
    """
    A class to represent an automation tool.
    """

    def __init__(self, name: str, version: str) -> None:
        """
        Initialize an automation tool with a name and version.
        
        :param name: The name of the automation tool.
        :param version: The version of the automation tool.
        """
        self.name = name
        self.version = version

    def run(self, task: str, params: Optional[Dict[str, Any]] = None) -> str:
        """
        Execute a task with the given parameters if provided.
        
        :param task: The task to run.
        :param params: A dictionary of parameters for the task.
        :return: A string describing the result of the task execution.
        """
        if params is None:
            params = {}
        return f"Running {task} with parameters {params} on {self.name} v{self.version}"

    def status(self) -> Dict[str, str]:
        """
        Get the status of the automation tool.
        
        :return: A dictionary containing the status of the tool.
        """
        return {"name": self.name, "version": self.version, "status": "active"}

# Example usage
if __name__ == '__main__':
    tool = AutomationTool(name='AutomationTool-14', version='1.0')
    print(tool.run('example_task', { 'key': 'value' }))
    print(tool.status())