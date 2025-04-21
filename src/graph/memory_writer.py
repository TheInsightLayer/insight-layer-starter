import os
import json
from src.memory.insight_layer_memory import InsightLayerMemory
# from jsonschema import validate, ValidationError  # Uncomment if using schema

def write_to_memory(insight: dict, validate_schema: bool = False):
    """
    Saves a structured insight to the Insight Layer memory system.

    Checks for duplicates and optionally validates against a JSON schema.

    Parameters:
        insight (dict): The insight to store.
        validate_schema (bool): Whether to validate the insight against a schema before saving.
    """

    memory = InsightLayerMemory(vault_path="data/memory.db")

    # Optional: validate schema (requires schema + jsonschema package)
    # if validate_schema:
    #     try:
    #         from configs.insight_unit_schema import schema  # make sure this exists
    #         validate(instance=insight, schema=schema)
    #     except ValidationError as ve:
    #         print("❗ Insight schema validation failed:", ve)
    #         return

    # Check for duplicates (same what + why + when)
    existing = memory.load_context({"purpose": insight.get("why", ""), "topic": insight.get("what", ""), "quarter": insight.get("when", "")})
    for e in existing:
        if (
            e.get("what") == insight.get("what") and
            e.get("why") == insight.get("why") and
            e.get("when") == insight.get("when")
        ):
            print("Duplicate insight found. Skipping save.")
            return

    # Save insight
    memory.save_context(insight)
    print("Insight saved.")
