
import json
from datetime import datetime
import os

class MemoryTraceLogger:
    def __init__(self, path="data/memory_trace.log"):
        self.path = path
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

    def log(self, event: dict):
        event["timestamp"] = datetime.now().isoformat()
        with open(self.path, "a") as f:
            f.write(json.dumps(event) + "\n")
