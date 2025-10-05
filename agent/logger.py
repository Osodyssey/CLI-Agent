import os
import json
from .config import LOG_FILE

def ensure_log_dir():
    d = os.path.dirname(LOG_FILE)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)

def log_step(data):
    ensure_log_dir()
    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    except Exception:
        logs = []
    logs.append(data)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)
