import yaml
import os

CONFIG_PATH = "configs/importance_weights.yaml"

def load_weights():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return yaml.safe_load(f)
    return {
        "used": 0.4,
        "links": 0.3,
        "impact": 0.1,
        "outcome": 0.1,
        "recency": 0.1
    }

def save_weights(weights):
    os.makedirs("configs", exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        yaml.dump(weights, f)
