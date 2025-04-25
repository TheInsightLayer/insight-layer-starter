
# Loads YAML config and runs the LangGraph insight agent end-to-end

import yaml
import sys
from agents.insight_layer_langgraph_full_agent import insight_agent_graph  
from dotenv import load_dotenv
from src.memory.insight_layer_memory import InsightLayerMemory

load_dotenv()
memory = InsightLayerMemory()

def run_from_config(config_path="configs/insight_agent_config.yaml"):
    # Load YAML config file containing task + options
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    # Validate required fields
    required_keys = ["task", "task_meta"]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required config key: '{key}'")

    # Set defaults for optional fields
    config.setdefault("normalize_fields", True)

    # Run the compiled LangGraph agent using the config as state
    result = insight_agent_graph.invoke(config)

    # Print the agent's main output
    print("Agent Output:\n", result["agent_output"])

    # Show the structured insight that was saved
    print("\nInsight Saved:\n", result["saved_insight"])

    # Example: Increment usage when an insight is retrieved
    retrieved_insights = result.get("retrieved_insights", [])
    for insight_id in retrieved_insights:
        memory.increment_usage(insight_id)
        print(f"Insight {insight_id} usage incremented.")

    # Show whether a bundle was updated (if auto_bundle was enabled)
    if result.get("bundle_updated"):
        print("\nBundle Updated:", result["bundle_updated"])
    else:
        print("\nNo bundle update.")

# Run from CLI
if __name__ == "__main__":
    config_file = sys.argv[1] if len(sys.argv) > 1 else "configs/insight_agent_config.yaml"
    run_from_config(config_file)
