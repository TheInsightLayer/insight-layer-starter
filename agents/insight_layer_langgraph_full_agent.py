
"""
LangGraph Agent: Insight Layer Flow (Normalized Schema Version)

This agent supports memory reuse, insight creation, trace logging, and auto-bundling.
All outputs follow the normalized InsightUnit schema.

Key Features:
- Loads past insights via InsightMemoryTool
- Constructs prompts using reusable memory
- Summarizes and stores the output as a normalized InsightUnit
- Logs trace history and bundles by topic

Schema fields like `confidence_level` have been renamed to `level`, etc.
"""

from langgraph.graph import StateGraph, END
from langchain.schema import SystemMessage
from langchain_openai import ChatOpenAI
from tools.insight_memory_tool import InsightMemoryTool
from src.graph.dynamic_prompt_builder import build_dynamic_prompt

import os
import json
from datetime import datetime

llm = ChatOpenAI(model="gpt-4", temperature=0.3)
memory = InsightMemoryTool()
tools = memory.as_langchain_tools()

BUNDLE_PATH = "data/bundles"
TRACE_PATH = "data/trace_logs"

def fetch_context_node(state):
    task_meta = state["task_meta"]
    all_insights = memory.load_context(task_meta)
    if state.get("confidential_only"):
        filtered = [i for i in all_insights if i.get("confidentiality", "public") == "team_only"]
        state["prior_insights"] = filtered
    else:
        state["prior_insights"] = all_insights
    return state

def run_agent_node(state):
    task = state["task"]
    task_meta = state["task_meta"]
    insights = state.get("prior_insights", [])

    prompt = build_dynamic_prompt(task, insights, task_meta)
    response = llm.predict(prompt)
    state["agent_output"] = response
    return state

def save_insight_node(state):
    insight = memory.save_output_as_insight(state["agent_output"], state["task_meta"], normalize=True)
    state["saved_insight"] = insight
    return state

def trace_node(state):
    if not state.get("trace_enabled"):
        return state

    os.makedirs(TRACE_PATH, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    log_file = os.path.join(TRACE_PATH, f"trace_{timestamp}.json")

    with open(log_file, "w") as f:
        json.dump({
            "task": state["task"],
            "task_meta": state["task_meta"],
            "used_insights": state.get("prior_insights", []),
            "output": state["agent_output"]
        }, f, indent=2)

    return state

def bundle_insight_node(state):
    if not state.get("auto_bundle"):
        return state

    insight = state["saved_insight"]
    topic = state["task_meta"].get("topic")
    bundle_id = f"auto_bundle_{topic}"
    bundle_path = os.path.join(BUNDLE_PATH, f"{bundle_id}.json")

    os.makedirs(BUNDLE_PATH, exist_ok=True)

    if os.path.exists(bundle_path):
        with open(bundle_path, "r") as f:
            bundle = json.load(f)
    else:
        bundle = {
            "bundle_id": bundle_id,
            "name": f"Auto Bundle: {topic.title()}",
            "role": "general",
            "summary": f"Auto-collected insights for topic: {topic}",
            "insights": []
        }

    insight_id = insight.get("id") or insight.get("source", "unknown_id")
    if insight_id not in bundle["insights"]:
        bundle["insights"].append(insight_id)

    with open(bundle_path, "w") as f:
        json.dump(bundle, f, indent=2)

    state["bundle_updated"] = bundle_id
    return state

graph = StateGraph()
graph.add_node("fetch_context", fetch_context_node)
graph.add_node("run_agent", run_agent_node)
graph.add_node("save_insight", save_insight_node)
graph.add_node("log_trace", trace_node)
graph.add_node("bundle_if_enabled", bundle_insight_node)

graph.set_entry_point("fetch_context")
graph.add_edge("fetch_context", "run_agent")
graph.add_edge("run_agent", "save_insight")
graph.add_edge("save_insight", "log_trace")
graph.add_edge("log_trace", "bundle_if_enabled")
graph.set_finish_point("bundle_if_enabled")

insight_agent_graph = graph.compile()

if __name__ == "__main__":
    result = insight_agent_graph.invoke({
        "task": "Develop a Q1 promotion strategy",
        "task_meta": {
            "purpose": "campaign planning",
            "quarter": "Q1",
            "topic": "promotion"
        },
        "auto_bundle": True,
        "trace_enabled": True,
        "confidential_only": True
    })
    print("Agent result:", result["agent_output"])
    print("Insight saved:", result["saved_insight"])
    print("Bundle updated:", result.get("bundle_updated", "No bundling"))
