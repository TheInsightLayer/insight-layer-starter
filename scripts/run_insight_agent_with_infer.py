
import yaml
import os
import sys
from agents.insight_layer_langgraph_full_agent import insight_agent_graph
from dotenv import load_dotenv
load_dotenv()
# Try to import auto-infer tool
try:
    from tools.infer_task_meta_with_threshold import infer_task_meta
except ImportError:
    print("❗ Could not import infer_task_meta. Make sure it's in your PYTHONPATH.")
    sys.exit(1)

def run_from_config(config_path="configs/insight_agent_config.yaml"):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    if "task_meta" not in config or not config["task_meta"]:
        print("No task_meta found. Auto-inferring from task string...")
        inferred = infer_task_meta(config["task"])
        print("Inferred task_meta:", inferred)
        config["task_meta"] = inferred

    result = insight_agent_graph.invoke(config)
    print("Agent Output:\n", result["agent_output"])
    print("\nInsight Saved:\n", result["saved_insight"])
    if result.get("bundle_updated"):
        print("\nBundle Updated:", result["bundle_updated"])
    else:
        print("\nNo bundle update.")

if __name__ == "__main__":
    run_from_config()
