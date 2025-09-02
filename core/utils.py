import os
import json
from datetime import datetime

def ensure_dir(path: str):
    """Make sure directory exists, if not create it."""
    os.makedirs(path, exist_ok=True)
    return path

def save_json(data, path: str, indent: int = 2):
    """Save Python dict/list to JSON file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)

def load_json(path: str):
    """Load JSON file safely."""
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def log(message: str):
    """Simple timestamped logger."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

