import yaml
import os

def load_prompt_templates(path="configs/prompt_templates.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def get_prompt_for_purpose(purpose: str, templates: dict) -> dict:
    return templates.get(purpose, templates.get("default"))
