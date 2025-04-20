import os
import json
from datetime import datetime
from pathlib import Path

AUDIT_LOG_PATH = Path("data/audit_log.jsonl")

def log_event(action, insight_data):
    event = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "insight": insight_data
    }
    with open(AUDIT_LOG_PATH, "a") as f:
        f.write(json.dumps(event) + "\n")