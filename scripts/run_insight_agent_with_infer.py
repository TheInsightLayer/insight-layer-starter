import yaml
import os
import sys
from dotenv import load_dotenv
from agents.insight_layer_langgraph_full_agent import insight_agent_graph
from tools.infer_task_meta_with_threshold import infer_task_meta
from src.utils.insight_stubs import create_stub_insight
from src.memory.insight_layer_memory import InsightLayerMemory

load_dotenv()

memory = InsightLayerMemory()

def run_from_config(config_path="configs/insight_agent_config.yaml"):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    # STEP 1: Handle missing task_meta by inference
    if "task_meta" not in config or not config["task_meta"]:
        print("No task_meta found. Auto-inferring from task string...")
        inferred = infer_task_meta(config["task"])
        print("Inferred task_meta:", inferred)
        config["task_meta"] = inferred

    # STEP 2: Create a schema-compliant stub InsightUnit for tracking
    stub_insight = create_stub_insight(config["task"])
    memory.save_context(stub_insight.dict())
    print(f"Stub Insight saved with ID: {stub_insight.id}")

    # STEP 3: Run LangGraph agent with enriched config
    result = insight_agent_graph.invoke(config)

    print("Agent Output:\n", result["agent_output"])
    print("\nInsight Saved:\n", result["saved_insight"])

    if result.get("bundle_updated"):
        print("\nBundle Updated:", result["bundle_updated"])
    else:
        print("\nNo bundle update.")

if __name__ == "__main__":
    run_from_config()
