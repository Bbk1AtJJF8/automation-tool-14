import os
import json
import logging

def load_json(file_path):
    """Load JSON data from a file."""
    if not os.path.isfile(file_path):
        logging.error(f"File '{file_path}' not found.")
        return None
    with open(file_path, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON: {e}")
            return None


def save_json(data, file_path):
    """Save data as JSON to a file."""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)


def get_file_extension(file_name):
    """Return the file extension from a file name."""
    return os.path.splitext(file_name)[1]


def read_file_lines(file_path):
    """Read all lines from a file and return as a list."""
    if not os.path.isfile(file_path):
        logging.error(f"File '{file_path}' not found.")
        return []
    with open(file_path, 'r') as f:
        return f.readlines()


def write_lines_to_file(lines, file_path):
    """Write a list of lines to a file."""
    with open(file_path, 'w') as f:
        f.writelines(lines)
