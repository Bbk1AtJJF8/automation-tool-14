# automation-tool-14

A robust, high-performance automation engine designed to streamline repetitive file system tasks and system workflows. This utility provides a clean, Python-based interface for scheduling complex sequences and reducing manual overhead.

## Features

*   **Task Scheduling:** Execute granular background processes using a lightweight, non-blocking asynchronous event loop.
*   **File Watcher:** Real-time monitoring of local directories with instant trigger-based response actions for file changes.
*   **YAML Configuration:** Define complex automation pipelines through human-readable configuration files rather than hardcoded scripts.
*   **Multi-Platform Support:** Native compatibility across Linux, macOS, and Windows with minimal system dependencies.

## Installation

Ensure you have Python 3.9+ installed. You can install `automation-tool-14` directly via pip:

```bash
# Clone the repository
git clone https://github.com/Developer/automation-tool-14.git
cd automation-tool-14

# Install dependencies
pip install -r requirements.txt
```

## Usage

Create a `config.yaml` in the root directory to define your automation tasks:

```yaml
tasks:
  - name: "Cleanup"
    path: "./temp"
    action: "delete"
    schedule: "0 0 * * *"
```

Run the engine to initialize the monitor:

```bash
python main.py --config config.yaml --verbose
```

The tool will parse the configuration and begin tracking the specified directories according to your defined schedule.

## License

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.