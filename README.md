# automation-tool-14

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`automation-tool-14` is a lightweight Python library designed to streamline repetitive file operations, API polling, and system notification workflows. By consolidating boilerplate scripting logic into robust, async-ready utility modules, it allows developers to deploy reliable background workers in minutes.

## Features

* **Event-Driven File Watcher:** Monitor target directories for creation, modification, or deletion events and trigger custom Python callbacks.
* **Resilient API Poller:** Perform scheduled HTTP requests with built-in exponential backoff, retry logic, and JSON payload validation.
* **Cross-Platform Alerts:** Send native desktop notifications on macOS, Windows, and Linux with zero external system dependencies.

## Installation

Install the package directly from PyPI using pip:

```bash
pip install automation-tool-14
```

## Quick Start

The following example demonstrates how to monitor a directory for new CSV files and trigger a system notification when one is detected.

```python
import time
from automation_tool_14 import FileWatcher, Notifier

# Callback function when a new file is detected
def process_new_file(filepath):
    print(f"Detecting file: {filepath}")
    Notifier.send(
        title="File Automation", 
        message=f"Successfully processed {filepath}"
    )

# Initialize and start the directory watcher
watcher = FileWatcher(directory="./incoming", pattern="*.csv")
watcher.on_create(callback=process_new_file)

watcher.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    watcher.stop()
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.