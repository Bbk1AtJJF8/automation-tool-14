# Automation Tool 14

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)

`automation-tool-14` is a lightweight Python utility designed to eliminate repetitive file management and data-scraping chores. It streamlines everyday administrative workflows through configurable YAML pipelines and a robust CLI interface.

## Features

* **Configurable Pipelines:** Define complex multi-step workflows using straightforward YAML configuration files without writing boilerplate code.
* **Concurrent Execution:** Leverages Python's `asyncio` and `multiprocessing` to process large batches of local files or network requests in parallel.
* **Smart Error Recovery:** Automatically retries failed operations with exponential backoff and logs detailed stack traces for rapid debugging.
* **Extensible Plugin Architecture:** Easily write custom action modules to integrate internal APIs or proprietary file parsers into existing workflows.

## Installation

Ensure you have Python 3.8 or higher installed on your system. Clone the repository and install the package locally:

```bash
git clone https://github.com/Developer/automation-tool-14.git
cd automation-tool-14
pip install -e .
```

## Usage

To run the tool, supply a valid workflow configuration file using the command-line interface. 

1. Create a sample configuration file named `workflow.yaml`:
   ```yaml
   name: daily-cleanup
   tasks:
     - action: archive_logs
       source: /var/log/app/
       destination: /mnt/backups/
       max_age_days: 7
   ```

2. Execute the tool:
   ```bash
   auto14 run --config workflow.yaml
   ```

For a full list of available CLI commands and global flags, run:
```bash
auto14 --help
```

## License

This project is licensed under the terms of the [MIT License](LICENSE).