[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# automation-tool-14

`automation-tool-14` is a lightweight Python engine designed to streamline local file operations, scheduled system tasks, and event-driven workflows. It provides a simple declarative interface to execute custom scripts, manage file watchers, and aggregate task execution metrics with minimal overhead.

## Features

* **Declarative Workflows:** Define multi-step pipelines and conditional triggers using concise YAML configuration files.
* **Real-time File Watchers:** Monitor directories for file creation, modification, or deletion to execute targeted actions immediately.
* **Flexible Task Scheduler:** Execute background jobs on fixed intervals or custom cron schedules with built-in exponential backoff retries.
* **Structured Output Logging:** Stream execution states, task outputs, and error diagnostics directly to stdout or structured JSON log files.

## Installation

Install directly from source using Python 3.9 or higher:

```bash
git clone https://github.com/Developer/automation-tool-14.git
cd automation-tool-14
pip install -r requirements.txt
pip install -e .
```

## Basic Usage

Create a workflow file named `workflow.yaml`:

```yaml
name: File Processor
trigger:
  watch_directory: ./incoming
  pattern: "*.csv"
action:
  run_script: scripts/process_data.py
```

Execute the engine programmatically in Python:

```python
from automation_tool_14 import WorkflowEngine

# Initialize the engine with your workflow configuration
engine = WorkflowEngine(config_path="workflow.yaml")

# Start listening for triggers and running tasks
engine.start()
```

Or run via CLI:

```bash
automation-tool-14 run --config workflow.yaml
```

## License

This project is licensed under the [MIT License](LICENSE).