# run_langchain_agent.py

import yaml
from agents.insight_layer_langgraph_full_agent import insight_agent_graph

def run_from_yaml(config_path="configs/insight_agent_config.yaml"):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    result = insight_agent_graph.invoke(config)

    print("\n Agent Output:\n", result["agent_output"])
    print("\n Insight Saved:\n", result["saved_insight"])

    if result.get("bundle_updated"):
        print("\n Bundle Updated:", result["bundle_updated"])
    else:
        print("\n No bundle update.")

if __name__ == "__main__":
    config_path = sys.argv[1] if len(sys.argv) > 1 else "configs/insight_agent_config.yaml"
    run_from_yaml(config_path)
