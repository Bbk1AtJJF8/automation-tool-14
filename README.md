# automation-tool-14

`automation-tool-14` is a lightweight, high-performance Python framework designed to streamline repetitive cross-platform workflows. It provides a modular architecture that allows developers to automate complex shell interactions and data processing tasks with minimal overhead.

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

### Key Features

*   **Task Scheduling:** Built-in cron-style scheduling engine to trigger scripts based on time intervals or system events.
*   **Parallel Execution:** Multi-threaded worker pool to execute independent automation tasks concurrently, significantly reducing total runtime.
*   **Dynamic Configuration:** Seamless integration with YAML and JSON files to manage environment-specific variables without code changes.
*   **Extensible Hook System:** Plug-and-play architecture supporting custom pre-run and post-run hooks for logging and notification integration.

### Installation

Requires Python 3.8 or higher. Install the package directly via pip:

```bash
# Clone the repository
git clone https://github.com/Developer/automation-tool-14.git
cd automation-tool-14

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

You can initialize a new automation sequence by defining a configuration file and invoking the runner module:

```python
from automation_tool_14 import Runner

# Initialize the engine with a config file
engine = Runner(config_path='config/tasks.yaml')

# Execute defined sequences
engine.run()
```

For advanced CLI usage, execute the following command in your terminal:

```bash
python -m automation_tool_14 --execute --config ./tasks.yaml --verbose
```

### Configuration
Create a `tasks.yaml` in your root directory to define your tasks:
```yaml
tasks:
  - name: cleanup
    command: "rm -rf ./tmp/*"
    interval: "daily"
```

### License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.