import json
import os

def ensure_dir(file_path):
    """Ensures the directory for the given file path exists."""
    directory = os.path.dirname(file_path)
    if directory:
        os.makedirs(directory, exist_ok=True)

def read_json(file_path):
    """Reads a JSON file and returns the data. Raises FileNotFoundError if missing."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_json(data, file_path, indent=2):
    """Writes data to a JSON file, ensuring the directory exists."""
    ensure_dir(file_path)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent)

def read_lines(file_path):
    """Reads a text file and returns a list of non-empty lines. Raises FileNotFoundError if missing."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def write_lines(lines, file_path):
    """Writes a list of lines to a text file."""
    ensure_dir(file_path)
    with open(file_path, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(f"{line}\n")

def read_binary(file_path):
    """Reads binary data from a file. Raises FileNotFoundError if missing."""
    with open(file_path, 'rb') as f:
        return f.read()

def write_binary(data, file_path):
    """Writes binary data to a file, ensuring the directory exists."""
    ensure_dir(file_path)
    with open(file_path, 'wb') as f:
        f.write(data)
