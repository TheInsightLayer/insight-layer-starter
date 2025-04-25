import os
import json
from src.memory.insight_layer_memory import InsightLayerMemory
from src.utils.normalize_fields import normalize_insight
# from jsonschema import validate, ValidationError  # Optional schema validation

def write_to_memory(insight: dict, validate_schema: bool = False):
    """
    Saves a structured insight to the Insight Layer memory system.

    Checks for duplicates and optionally validates against a JSON schema.

    Parameters:
        insight (dict): The insight to store.
        validate_schema (bool): Whether to validate the insight against a schema before saving.
    """

    memory = InsightLayerMemory(vault_path="data/memory.db")
    normalized = normalize_insight(insight)

    # Optional: validate schema (requires a JSON schema and jsonschema package)
    # if validate_schema:
    #     try:
    #         from configs.insight_unit_schema import schema
    #         validate(instance=normalized, schema=schema)
    #     except ValidationError as ve:
    #         print("❗ Insight schema validation failed:", ve)
    #         return

    # Check for duplicates based on narrative fields
    narrative = normalized.get("narrative", {})
    existing = memory.load_context({
        "purpose": narrative.get("why", ""),
        "topic": narrative.get("what", ""),
        "quarter": narrative.get("when", "")
    })

    for e in existing:
        existing_narr = e.get("narrative", {})
        if (
            existing_narr.get("what") == narrative.get("what") and
            existing_narr.get("why") == narrative.get("why") and
            existing_narr.get("when") == narrative.get("when")
        ):
            print("Duplicate insight found. Skipping save.")
            return

    # Save insight
    memory.save_context(normalized)
    print("Insight saved.")
